#!/usr/bin/env python3
"""
Перевірка контейнера доріг (UARDS001): зведення, найближча дорога до точки,
вивантаження плитки в KML. Це водночас еталонний читач формату — Java-читач
у застосунку має робити те саме.

    python3 verify_roads.py ua-roads.bin                       # зведення
    python3 verify_roads.py ua-roads.bin --near 50.4501,30.5234 # найближчі дороги до точки
    python3 verify_roads.py ua-roads.bin --kml 50.45,30.52 out.kml   # плитка з цією точкою → KML
"""
import argparse
import math
import struct
import zlib

CLASS_NAMES = ['motorway', 'trunk', 'primary', 'secondary', 'tertiary', 'unclassified', 'residential',
               'living_street', 'service', 'motorway_link', 'trunk_link', 'primary_link', 'secondary_link',
               'tertiary_link', 'track']


class Roads:
    def __init__(self, path):
        self.f = open(path, 'rb')
        hdr = self.f.read(8 + 24)
        if hdr[:8] != b'UARDS001':
            raise SystemExit('не контейнер UARDS001')
        (self.version, self.tile, self.lat0, self.lon0, self.n_lat, self.n_lon) = struct.unpack('>iiiiii', hdr[8:])
        self.index = self.f.read(self.n_lat * self.n_lon * 12)

    def tile_of(self, lat, lon):
        """(ti, tj) — індекси плитки в сітці контейнера для координат у градусах, або None."""
        ti = math.floor(lat * 1e6 / self.tile) - self.lat0 // self.tile
        tj = math.floor(lon * 1e6 / self.tile) - self.lon0 // self.tile
        if 0 <= ti < self.n_lat and 0 <= tj < self.n_lon:
            return ti, tj
        return None

    def read_tile(self, ti, tj):
        """Список відрізків плитки: dict(cls, oneway, way, a, b, pts=[(lat, lon) у градусах])."""
        off, ln = struct.unpack('>qi', self.index[(ti * self.n_lon + tj) * 12:(ti * self.n_lon + tj) * 12 + 12])
        if ln == 0:
            return []
        self.f.seek(off)
        raw = zlib.decompress(self.f.read(ln))
        pos = 0

        def varint():
            nonlocal pos
            v, sh = 0, 0
            while True:
                b = raw[pos]
                pos += 1
                v |= (b & 0x7F) << sh
                if not b & 0x80:
                    return v
                sh += 7

        def svarint():
            v = varint()
            return (v >> 1) ^ -(v & 1)

        n = varint()
        out = []
        plat0 = self.lat0 + ti * self.tile
        plon0 = self.lon0 + tj * self.tile
        for _ in range(n):
            cls, ow = raw[pos], raw[pos + 1]
            pos += 2
            wid, na, nb, npts = varint(), varint(), varint(), varint()
            plat, plon = plat0, plon0
            pts = []
            for _ in range(npts):
                plat += svarint()
                plon += svarint()
                pts.append((plat / 1e6, plon / 1e6))
            out.append(dict(cls=cls, oneway=ow, way=wid, a=na, b=nb, pts=pts))
        return out

    def around(self, lat, lon):
        """Відрізки плиток 3×3 навколо точки, без дублікатів."""
        c = self.tile_of(lat, lon)
        if not c:
            return []
        seen, out = set(), []
        for di in (-1, 0, 1):
            for dj in (-1, 0, 1):
                ti, tj = c[0] + di, c[1] + dj
                if 0 <= ti < self.n_lat and 0 <= tj < self.n_lon:
                    for s in self.read_tile(ti, tj):
                        k = (s['way'], s['a'], s['b'])
                        if k not in seen:
                            seen.add(k)
                            out.append(s)
        return out


def dist_to_segment(lat, lon, pts):
    """Найменша відстань (м) від точки до ламаної і індекс ланки."""
    cos = math.cos(math.radians(lat))
    k = 111319.5
    px, py = lon * k * cos, lat * k
    best, bi = float('inf'), -1
    for i in range(len(pts) - 1):
        ax, ay = pts[i][1] * k * cos, pts[i][0] * k
        bx, by = pts[i + 1][1] * k * cos, pts[i + 1][0] * k
        dx, dy = bx - ax, by - ay
        L2 = dx * dx + dy * dy
        t = 0 if L2 == 0 else max(0.0, min(1.0, ((px - ax) * dx + (py - ay) * dy) / L2))
        d = math.hypot(px - (ax + t * dx), py - (ay + t * dy))
        if d < best:
            best, bi = d, i
    return best, bi


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('path')
    ap.add_argument('--near', help='lat,lon — 5 найближчих доріг')
    ap.add_argument('--kml', nargs=2, metavar=('LAT,LON', 'OUT.kml'), help='плитка з точкою → KML')
    a = ap.parse_args()
    r = Roads(a.path)
    print(f'версія {r.version}, плитка {r.tile / 1e6}°, кут ({r.lat0 / 1e6}, {r.lon0 / 1e6}), сітка {r.n_lat}×{r.n_lon}')
    if not a.near and not a.kml:
        nonempty = 0
        by_cls = [0] * len(CLASS_NAMES)
        segs = pts = 0
        for ti in range(r.n_lat):
            for tj in range(r.n_lon):
                t = r.read_tile(ti, tj)
                if t:
                    nonempty += 1
                for s in t:
                    segs += 1
                    pts += len(s['pts'])
                    by_cls[s['cls']] += 1
        print(f'непорожніх плиток {nonempty}, відрізків {segs} (з дублюванням на межах), точок {pts}')
        for i, n in enumerate(by_cls):
            if n:
                print(f'  {CLASS_NAMES[i]:16s} {n}')
    if a.near:
        lat, lon = map(float, a.near.split(','))
        cand = []
        for s in r.around(lat, lon):
            d, i = dist_to_segment(lat, lon, s['pts'])
            cand.append((d, s, i))
        cand.sort(key=lambda x: x[0])
        for d, s, i in cand[:5]:
            print(f'  {d:7.1f} м  {CLASS_NAMES[s["cls"]]:14s} way {s["way"]} вузли {s["a"]}–{s["b"]} oneway={s["oneway"]} точок {len(s["pts"])}')
    if a.kml:
        lat, lon = map(float, a.kml[0].split(','))
        c = r.tile_of(lat, lon)
        if not c:
            raise SystemExit('точка поза контейнером')
        col = {0: 'ff0000ff', 1: 'ff0000ff', 2: 'ff0080ff', 3: 'ff00c8ff', 4: 'ff00c800', 5: 'ff808080', 6: 'ff404040',
               7: 'ff404040', 8: 'ffc0c0c0', 14: 'ff60a0a0'}
        with open(a.kml[1], 'w', encoding='utf-8') as f:
            f.write('<?xml version="1.0" encoding="UTF-8"?><kml xmlns="http://www.opengis.net/kml/2.2"><Document>')
            for s in r.read_tile(*c):
                f.write(f'<Placemark><name>{CLASS_NAMES[s["cls"]]} {s["way"]}</name><Style><LineStyle><color>{col.get(s["cls"], "ff0080ff")}</color><width>2</width></LineStyle></Style>'
                        f'<LineString><coordinates>{" ".join(f"{lo:.6f},{la:.6f},0" for la, lo in s["pts"])}</coordinates></LineString></Placemark>')
            f.write('</Document></kml>')
        print('записано', a.kml[1])


if __name__ == '__main__':
    main()
