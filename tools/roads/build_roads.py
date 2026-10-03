#!/usr/bin/env python3
"""
OSM (.osm.pbf / .osm) → компактний контейнер доріг для GNSS Filter (формат UARDS001,
див. FORMAT.md). Лише дороги для авто; геометрія спрощена; шляхи порізано на
відрізки між перехрестями; плитки 0,1° × 0,1°, кожна стиснута zlib.

Використання:
    python3 build_roads.py ukraine-roads.osm.pbf ua-roads.bin
    python3 build_roads.py ukraine-roads.osm.pbf kyiv-roads.bin --bbox 49.5,29.0,51.5,32.0
    python3 build_roads.py ... --tolerance 2 --no-track

Вхід краще попередньо відфільтрувати osmium-tool (у сотні разів менше даних):
    osmium tags-filter ukraine-latest.osm.pbf w/highway -o ukraine-roads.osm.pbf

Залежності: pip install osmium numpy
"""
import argparse
import math
import struct
import sys
import time
import zlib
from collections import defaultdict

import numpy as np
import osmium

# --------------------------------------------------------------------- класи
CLASSES = {
    'motorway': 0, 'trunk': 1, 'primary': 2, 'secondary': 3, 'tertiary': 4,
    'unclassified': 5, 'residential': 6, 'living_street': 7, 'service': 8,
    'motorway_link': 9, 'trunk_link': 10, 'primary_link': 11, 'secondary_link': 12, 'tertiary_link': 13,
    'track': 14,
}
TILE_UDEG = 25_000             # 0,025° у мікроградусах (≈2,8 × 1,8 км); --tile змінює
# Не беремо (службові, де авто не «їде дорогою»): проходи стоянок і drive-through.
SKIP_SERVICE = {'parking_aisle', 'drive-through', 'drive_through', 'emergency_access'}
MAGIC = b'UARDS001'


def zigzag(v: int) -> int:
    return (v << 1) ^ (v >> 63)


def put_varint(buf: bytearray, v: int) -> None:
    """Беззнаковий varint (LEB128), як у protobuf."""
    while True:
        b = v & 0x7F
        v >>= 7
        if v:
            buf.append(b | 0x80)
        else:
            buf.append(b)
            return


def put_svarint(buf: bytearray, v: int) -> None:
    put_varint(buf, zigzag(v))


# ---------------------------------------------------------- спрощення (DP)
def simplify(pts, tol_m):
    """Дуглас–Пекер у метрах; кінці завжди лишаються. pts — список (lat_udeg, lon_udeg)."""
    if len(pts) <= 2 or tol_m <= 0:
        return pts
    cos = math.cos(math.radians(pts[0][0] / 1e6))
    ky, kx = 0.1113195, 0.1113195 * cos      # м на мікроградус
    keep = [False] * len(pts)
    keep[0] = keep[-1] = True
    stack = [(0, len(pts) - 1)]
    while stack:
        a, b = stack.pop()
        if b - a < 2:
            continue
        ax, ay = pts[a][1] * kx, pts[a][0] * ky
        bx, by = pts[b][1] * kx, pts[b][0] * ky
        dx, dy = bx - ax, by - ay
        L2 = dx * dx + dy * dy
        best, bi = -1.0, -1
        for i in range(a + 1, b):
            px, py = pts[i][1] * kx - ax, pts[i][0] * ky - ay
            if L2 > 0:
                t = max(0.0, min(1.0, (px * dx + py * dy) / L2))
                ex, ey = px - t * dx, py - t * dy
            else:
                ex, ey = px, py
            d = ex * ex + ey * ey
            if d > best:
                best, bi = d, i
        if best > tol_m * tol_m:
            keep[bi] = True
            stack.append((a, bi))
            stack.append((bi, b))
    return [p for p, k in zip(pts, keep) if k]


def wanted(tags, keep_track):
    """Клас дороги або None."""
    hw = tags.get('highway')
    if hw not in CLASSES or (hw == 'track' and not keep_track):
        return None
    if tags.get('area') == 'yes':
        return None
    if hw == 'service' and tags.get('service') in SKIP_SERVICE:
        return None
    return CLASSES[hw]


def oneway_of(tags):
    """0 — ні; 1 — у напрямку точок; 2 — проти.
    Кільця (junction=roundabout/circular) і motorway односторонні й без тегу oneway:
    в OSM їх малюють у напрямку руху, тож напрямок — з самої лінії."""
    ow = tags.get('oneway', '')
    if ow in ('yes', 'true', '1'):
        return 1
    if ow == '-1':
        return 2
    if ow in ('no', 'false', '0', 'reversible', 'alternating'):
        return 0
    if tags.get('junction') in ('roundabout', 'circular'):
        return 1
    if tags.get('highway') == 'motorway':
        return 1
    return 0


# ------------------------------------------------------------- прохід 1
class Pass1(osmium.SimpleHandler):
    """Збирає всі node-id доріг, які беремо, — щоб знайти перехрестя."""

    def __init__(self, keep_track):
        super().__init__()
        self.keep_track = keep_track
        self.refs = []          # np.int64 chunks
        self.cur = []
        self.n_ways = 0

    def way(self, w):
        if wanted(w.tags, self.keep_track) is None:
            return
        self.n_ways += 1
        for n in w.nodes:
            self.cur.append(n.ref)
        if len(self.cur) > 2_000_000:
            self.refs.append(np.array(self.cur, dtype=np.int64))
            self.cur = []

    def junctions(self):
        if self.cur:
            self.refs.append(np.array(self.cur, dtype=np.int64))
        if not self.refs:
            return np.zeros(0, dtype=np.int64)
        allref = np.concatenate(self.refs)
        u, c = np.unique(allref, return_counts=True)
        return u[c >= 2]        # вузол у ≥2 шляхах (або двічі в одному) — перехрестя


# ------------------------------------------------------------- прохід 2
class Pass2(osmium.SimpleHandler):
    def __init__(self, junctions, keep_track, tol_m, bbox, tile):
        super().__init__()
        self.tile = tile
        self.j = junctions
        self.keep_track = keep_track
        self.tol = tol_m
        self.bbox = bbox        # (minlat, minlon, maxlat, maxlon) або None
        self.tiles = defaultdict(list)   # (ti, tj) -> [segment bytes]
        self.n_seg = 0
        self.n_pts_in = 0
        self.n_pts_out = 0
        self.n_dropped = 0

    def junction_mask(self, refs):
        """Векторно: які з refs — перехрестя."""
        r = np.asarray(refs, dtype=np.int64)
        if not len(self.j):
            return np.zeros(len(r), dtype=bool)
        i = np.searchsorted(self.j, r)
        i = np.minimum(i, len(self.j) - 1)
        return self.j[i] == r

    def way(self, w):
        cls = wanted(w.tags, self.keep_track)
        if cls is None:
            return
        oneway = oneway_of(w.tags)
        pts, refs = [], []
        for n in w.nodes:
            if not n.location.valid():
                # вузол без координат (обрізаний витяг) — розриваємо тут
                self._emit(w.id, cls, oneway, pts, refs)
                pts, refs = [], []
                continue
            pts.append((int(round(n.location.lat * 1e6)), int(round(n.location.lon * 1e6))))
            refs.append(n.ref)
        self._emit(w.id, cls, oneway, pts, refs)

    def _emit(self, wid, cls, oneway, pts, refs):
        if len(pts) < 2:
            return
        # різати на відрізки між перехрестями
        m = self.junction_mask(refs)
        cut = [0] + [i for i in range(1, len(refs) - 1) if m[i]] + [len(refs) - 1]
        for a, b in zip(cut, cut[1:]):
            self._segment(wid, cls, oneway, pts[a:b + 1], refs[a], refs[b])

    def _segment(self, wid, cls, oneway, pts, na, nb):
        self.n_pts_in += len(pts)
        if self.bbox:
            mnla, mnlo, mxla, mxlo = self.bbox
            if all(p[0] < mnla or p[0] > mxla or p[1] < mnlo or p[1] > mxlo for p in pts):
                self.n_dropped += 1
                return
        pts = simplify(pts, self.tol)
        self.n_pts_out += len(pts)
        lats = [p[0] for p in pts]
        lons = [p[1] for p in pts]
        T = self.tile
        ti0, ti1 = math.floor(min(lats) / T), math.floor(max(lats) / T)
        tj0, tj1 = math.floor(min(lons) / T), math.floor(max(lons) / T)
        self.n_seg += 1
        # відрізок потрапляє в кожну плитку, яку торкається його рамка (дублювання —
        # щоб пошук у 3×3 плитках навколо себе бачив і довгі відрізки траси)
        for ti in range(ti0, ti1 + 1):
            for tj in range(tj0, tj1 + 1):
                buf = bytearray()
                buf.append(cls)
                buf.append(oneway)
                put_varint(buf, wid)
                put_varint(buf, na)
                put_varint(buf, nb)
                put_varint(buf, len(pts))
                plat, plon = ti * T, tj * T
                for la, lo in pts:
                    put_svarint(buf, la - plat)
                    put_svarint(buf, lo - plon)
                    plat, plon = la, lo
                self.tiles[(ti, tj)].append(bytes(buf))


# ------------------------------------------------------------------- запис
def write_container(path, tiles, tile=TILE_UDEG):
    if not tiles:
        sys.exit('немає жодного відрізка — перевірте вхідний файл / bbox')
    tis = [t[0] for t in tiles]
    tjs = [t[1] for t in tiles]
    ti0, ti1, tj0, tj1 = min(tis), max(tis), min(tjs), max(tjs)
    n_lat, n_lon = ti1 - ti0 + 1, tj1 - tj0 + 1
    header = MAGIC + struct.pack('>iiiiii', 1, tile, ti0 * tile, tj0 * tile, n_lat, n_lon)
    index_len = n_lat * n_lon * 12
    body = bytearray()
    index = bytearray()
    raw_total = 0
    base = len(header) + index_len
    for ti in range(ti0, ti1 + 1):
        for tj in range(tj0, tj1 + 1):
            segs = tiles.get((ti, tj))
            if not segs:
                index += struct.pack('>qi', 0, 0)
                continue
            raw = bytearray()
            put_varint(raw, len(segs))
            for s in segs:
                raw += s
            raw_total += len(raw)
            comp = zlib.compress(bytes(raw), 9)
            index += struct.pack('>qi', base + len(body), len(comp))
            body += comp
    with open(path, 'wb') as f:
        f.write(header)
        f.write(index)
        f.write(body)
    return n_lat, n_lon, len(header) + index_len + len(body), raw_total


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('src', help='вхід: .osm.pbf або .osm (бажано вже відфільтрований по highway)')
    ap.add_argument('dst', help='вихід: контейнер .bin')
    ap.add_argument('--bbox', help='minlat,minlon,maxlat,maxlon — лишити лише цю рамку', default=None)
    ap.add_argument('--tolerance', type=float, default=2.0, help='допуск спрощення геометрії, м (типово 2)')
    ap.add_argument('--no-track', action='store_true', help='не брати highway=track (польові/лісові)')
    ap.add_argument('--tile', type=float, default=TILE_UDEG / 1e6, help='розмір плитки, ° (типово 0.025)')
    a = ap.parse_args()
    bbox = None
    if a.bbox:
        v = [float(x) for x in a.bbox.split(',')]
        if len(v) != 4:
            sys.exit('--bbox: потрібно 4 числа')
        bbox = (int(v[0] * 1e6), int(v[1] * 1e6), int(v[2] * 1e6), int(v[3] * 1e6))
    keep_track = not a.no_track

    t0 = time.time()
    p1 = Pass1(keep_track)
    p1.apply_file(a.src)
    junctions = p1.junctions()
    print(f'прохід 1: доріг {p1.n_ways}, перехресть {len(junctions)}, {time.time() - t0:.0f} с', flush=True)

    tile = int(round(a.tile * 1e6))
    if tile < 5000 or tile > 1_000_000:
        sys.exit('--tile: від 0.005 до 1')
    p2 = Pass2(junctions, keep_track, a.tolerance, bbox, tile)
    p2.apply_file(a.src, locations=True, idx='flex_mem')
    print(f'прохід 2: відрізків {p2.n_seg}, точок {p2.n_pts_in} → {p2.n_pts_out} після спрощення, '
          f'поза рамкою {p2.n_dropped}, плиток {len(p2.tiles)}, {time.time() - t0:.0f} с', flush=True)

    n_lat, n_lon, size, raw = write_container(a.dst, p2.tiles, tile)
    print(f'записано {a.dst}: сітка {n_lat}×{n_lon} плиток по {tile / 1e6}°, {size / 1e6:.1f} МБ '
          f'(без стиснення {raw / 1e6:.1f} МБ), {time.time() - t0:.0f} с')


if __name__ == '__main__':
    main()
