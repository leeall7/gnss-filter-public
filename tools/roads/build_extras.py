#!/usr/bin/env python3
"""
OSM → доповнення до доріг (формати UAREX001 і UAREX002, див. FORMAT_EXTRAS.md): обмеження швидкості за ідентифікатором
дороги OSM (у напрямку точок і проти) і точки — камери, залізничні переїзди, лежачі поліцейські. UAREX002 (з 0.9.3
GNSS Nav iOS) додає камерам напрямок: з тегів `direction` / `camera:direction` (градуси, сторони світу — вісь, куди
дивиться камера; `forward` / `backward` — напрямок руху вздовж дороги, як у highway=stop) і з відношень
`type=enforcement` + `enforcement=maxspeed` (ролі device / from / to — напрямок руху from → to).
Файл доріг ua-roads.bin (UARDS001) цей скрипт НЕ змінює: застосунок, якому доповнення не потрібні, їх просто
не завантажує. UAREX001 лишається для старих застосунків (окремий файл ua-extras.bin; UAREX002 — ua-extras2.bin).

Вхід — повний витяг або відфільтрований так (камери часто — окремі точки поза дорогою, тому w/highway мало; для
напрямку — ще й відношення enforcement із членами):
    osmium tags-filter ukraine-latest.osm.pbf w/highway n/highway=speed_camera n/enforcement r/enforcement \\
        n/railway=level_crossing n/traffic_calming -o extras-src.osm.pbf
Використання:
    python3 build_extras.py extras-src.osm.pbf ua-extras.bin                       # UAREX001 (як було)
    python3 build_extras.py extras-src.osm.pbf ua-extras2.bin --format 2           # UAREX002 (з напрямком камер)
    python3 build_extras.py extras-src.osm.pbf kyiv-extras.bin --bbox 49.3,29.2,51.6,32.2
Залежності: pip install osmium
"""
import argparse, math, struct, sys, zlib
import osmium

MAGIC = {1: b'UAREX001', 2: b'UAREX002'}
# ті самі класи доріг, що й build_roads.py: обмеження лише для доріг, які є в UARDS001
CLASSES = {'motorway', 'trunk', 'primary', 'secondary', 'tertiary', 'unclassified', 'residential', 'living_street',
           'service', 'motorway_link', 'trunk_link', 'primary_link', 'secondary_link', 'tertiary_link', 'track'}
UA_ZONE = {'UA:urban': 50, 'UA:rural': 90, 'UA:motorway': 130, 'UA:trunk': 110, 'UA:living_street': 20}
POI_CAMERA, POI_RAIL, POI_BUMP = 1, 2, 3
CALMING = {'bump', 'hump', 'table', 'cushion', 'yes', 'dip', 'chicane'}
# напрямок камери в UAREX002
DIR_NONE, DIR_AXIS, DIR_TRAVEL = 0, 1, 2
CARD = {'N': 0, 'NNE': 22.5, 'NE': 45, 'ENE': 67.5, 'E': 90, 'ESE': 112.5, 'SE': 135, 'SSE': 157.5, 'S': 180,
        'SSW': 202.5, 'SW': 225, 'WSW': 247.5, 'W': 270, 'WNW': 292.5, 'NW': 315, 'NNW': 337.5}


def speed_of(v):
    if not v: return 0
    v = v.strip()
    if v in UA_ZONE: return UA_ZONE[v]
    if v == 'walk': return 5
    num = ''.join(ch for ch in v.split(';')[0] if ch.isdigit())
    if not num: return 0
    k = int(num)
    if 'mph' in v: k = round(k * 1.609)
    return k if 5 <= k <= 150 else 0


def limits(t):
    base = speed_of(t.get('maxspeed')) or UA_ZONE.get(t.get('maxspeed:type', ''), 0) or UA_ZONE.get(t.get('source:maxspeed', ''), 0)
    return (speed_of(t.get('maxspeed:forward')) or base, speed_of(t.get('maxspeed:backward')) or base)


def poi_kind(t):
    if t.get('highway') == 'speed_camera' or t.get('enforcement') == 'maxspeed': return POI_CAMERA
    # лише переїзд «дорога × залізниця»; railway=crossing — пішохідний перехід через колію
    if t.get('railway') == 'level_crossing': return POI_RAIL
    if t.get('traffic_calming') in CALMING: return POI_BUMP
    return 0


def parse_dir(v):
    """Тег напрямку камери → градуси (вісь) | 'forward' | 'backward' | None (невідомо, кілька, обидва)."""
    if not v: return None
    v = v.strip()
    lo = v.lower()
    if lo in ('forward', 'backward'): return lo
    if lo in ('both', 'all', 'any'): return None
    if ';' in v or ',' in v: return None                         # кілька напрямків — невідомо (камера на обидва боки)
    if '-' in v[1:]: return None                                 # діапазон «0-90» — невідомо
    u = v.upper()
    if u in CARD: return float(CARD[u])
    try:
        d = float(v)
    except ValueError:
        return None
    return d % 360.0 if math.isfinite(d) else None


def bearing(la1, lo1, la2, lo2):
    """Азимут точка 1 → точка 2, ° (0 — північ, за годинниковою стрілкою); None, якщо точки збігаються."""
    k = math.cos(math.radians((la1 + la2) / 2))
    e, n = (lo2 - lo1) * k, (la2 - la1)
    if abs(e) < 1e-9 and abs(n) < 1e-9: return None
    return math.degrees(math.atan2(e, n)) % 360.0


def adiff(a, b):
    return abs((a - b + 180.0) % 360.0 - 180.0)


def circ_mean(v):
    x = sum(math.sin(math.radians(a)) for a in v); y = sum(math.cos(math.radians(a)) for a in v)
    return math.degrees(math.atan2(x, y)) % 360.0


def resolve(brs):
    """Кілька напрямків руху для однієї камери → (dirKind, градуси): збіжні (±30°) — рух; протилежні (180 ± 30°) — вісь
    (камера на обидва боки); інакше — невідомо."""
    if not brs: return DIR_NONE, 0
    if all(adiff(b, brs[0]) <= 30 for b in brs): return DIR_TRAVEL, int(round(circ_mean(brs))) % 360
    if all(adiff(b, brs[0]) <= 30 or adiff(b, brs[0]) >= 150 for b in brs): return DIR_AXIS, int(round(brs[0])) % 360
    return DIR_NONE, 0


def put_varint(buf, v):
    while True:
        b = v & 0x7F
        v >>= 7
        if v: buf.append(b | 0x80)
        else:
            buf.append(b); return


def put_svarint(buf, v): put_varint(buf, (v << 1) ^ (v >> 63))


class H(osmium.SimpleHandler):
    """Перший прохід (з координатами вузлів у дорогах): точки, обмеження, азимут дороги біля камер forward/backward,
    відношення enforcement."""
    def __init__(self, bbox):
        super().__init__()
        self.bbox = bbox
        self.lim = {}            # wayId → (fwd, bwd)
        self.pois = {}           # nodeId → [lat_udeg, lon_udeg, kind, maxspeed, dirKind, dirDeg]
        self.fb = {}             # nodeId камери → 'forward' | 'backward' (потрібен азимут дороги)
        self.fbBr = {}           # nodeId камери → [азимут руху з кожної дороги вузла]
        self.enf = []            # (maxspeed, [device nodeIds], from nodeId | None, to nodeId | None)

    def inside(self, la, lo):
        return not self.bbox or (self.bbox[0] <= la <= self.bbox[2] and self.bbox[1] <= lo <= self.bbox[3])

    def node(self, n):
        k = poi_kind(n.tags)
        if not k or not n.location.valid(): return
        la, lo = int(round(n.location.lat * 1e6)), int(round(n.location.lon * 1e6))
        if not self.inside(la, lo): return
        dk, dd = DIR_NONE, 0
        if k == POI_CAMERA:
            d = parse_dir(n.tags.get('direction')) if 'direction' in n.tags else parse_dir(n.tags.get('camera:direction'))
            if isinstance(d, float):
                dk, dd = DIR_AXIS, int(round(d)) % 360
            elif d in ('forward', 'backward'):
                self.fb[n.id] = d
        self.pois[n.id] = [la, lo, k, min(255, speed_of(n.tags.get('maxspeed'))), dk, dd]

    def way(self, w):
        t = w.tags
        if t.get('highway') not in CLASSES or t.get('area') == 'yes': return
        f, b = limits(t)
        if f or b: self.lim[w.id] = (min(255, f), min(255, b))
        if not self.fb: return
        nodes = w.nodes
        for i, nr in enumerate(nodes):
            sense = self.fb.get(nr.ref)
            if sense is None or nr.ref not in self.pois: continue
            a, c = nodes[max(0, i - 1)], nodes[min(len(nodes) - 1, i + 1)]
            if not (a.location.valid() and c.location.valid()): continue
            br = bearing(a.location.lat, a.location.lon, c.location.lat, c.location.lon)
            if br is None: continue
            if sense == 'backward': br = (br + 180.0) % 360.0
            self.fbBr.setdefault(nr.ref, []).append(br)        # вузол на кількох дорогах (перехрестя) — вирішимо в кінці

    def relation(self, r):
        t = r.tags
        if t.get('type') != 'enforcement' or t.get('enforcement') != 'maxspeed': return
        dev, fr, to = [], None, None
        for m in r.members:
            if m.type != 'n': continue
            if m.role == 'device': dev.append(m.ref)
            elif m.role == 'from' and fr is None: fr = m.ref
            elif m.role == 'to' and to is None: to = m.ref
        # за вікі OSM (Relation:enforcement) from — обов'язковий, to — за потреби; напрямок руху — від from (або device)
        # до to (або device); потрібні щонайменше дві різні точки
        if dev and (fr is not None or to is not None):
            self.enf.append((min(255, speed_of(t.get('maxspeed'))), dev, fr, to))


class Loc(osmium.SimpleHandler):
    """Другий прохід — координати вузлів, на які посилаються відношення enforcement."""
    def __init__(self, ids):
        super().__init__()
        self.ids = ids
        self.loc = {}

    def node(self, n):
        if n.id in self.ids and n.location.valid():
            self.loc[n.id] = (n.location.lat, n.location.lon)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('src'); ap.add_argument('dst')
    ap.add_argument('--bbox', default=None, help='minlat,minlon,maxlat,maxlon — точки лише в рамці (обмеження — усі)')
    ap.add_argument('--format', type=int, default=1, choices=(1, 2), help='1 — UAREX001 (як було), 2 — UAREX002 з напрямком камер')
    a = ap.parse_args()
    bbox = None
    if a.bbox:
        v = [float(x) for x in a.bbox.split(',')]
        if len(v) != 4: sys.exit('--bbox: потрібно 4 числа')
        bbox = tuple(int(x * 1e6) for x in v)
    h = H(bbox)
    h.apply_file(a.src, locations=(a.format == 2))
    # forward / backward: вузол на кількох дорогах з різним напрямком (перехрестя) — невідомо (resolve)
    for nid, brs in h.fbBr.items():
        p = h.pois.get(nid)
        if p is not None and p[4] == DIR_NONE: p[4], p[5] = resolve(brs)
    n_rel = 0
    if a.format == 2 and h.enf:
        need = set()
        for _, dev, fr, to in h.enf: need.update(dev); need.add(to); need.update([fr] if fr is not None else [])
        lh = Loc(need)
        lh.apply_file(a.src, locations=False)
        relBr = {}                                          # device → [азимути руху з усіх його відношень]
        for ms, dev, fr, to in h.enf:
            for d in dev:
                if d not in lh.loc: continue
                start = lh.loc.get(fr) if fr is not None else lh.loc[d]
                end = lh.loc.get(to) if to is not None else lh.loc[d]
                if start is None or end is None: continue
                # камера може стояти на стовпі збоку дороги: якщо одна з точок — сама камера, вона має бути далеко (≥ 50 м),
                # щоб бічний зсув не перекосив напрямок (10 м убік на 50 м — 11°); from і to обидві на дорозі — від 5 м
                dist = math.hypot((end[0] - start[0]) * 111320.0, (end[1] - start[1]) * 111320.0 * math.cos(math.radians(start[0])))
                if dist < (5.0 if fr is not None and to is not None and d not in (fr, to) else 50.0): continue
                br = bearing(start[0], start[1], end[0], end[1])
                if br is None: continue
                la, lo = int(round(lh.loc[d][0] * 1e6)), int(round(lh.loc[d][1] * 1e6))
                p = h.pois.get(d)
                if p is None:
                    if not h.inside(la, lo): continue
                    p = h.pois[d] = [la, lo, POI_CAMERA, ms, DIR_NONE, 0]
                if p[2] != POI_CAMERA: continue
                if not p[3] and ms: p[3] = ms
                relBr.setdefault(d, []).append(br)
        # камера на обидва боки — два відношення (вікі OSM, приклад 4): протилежні напрямки → вісь; відношення важать
        # більше за тег вузла
        for d, brs in relBr.items():
            p = h.pois[d]
            p[4], p[5] = resolve(brs)
            n_rel += 1
    body = bytearray()
    prev = 0
    for wid in sorted(h.lim):
        put_varint(body, wid - prev); prev = wid
        body.append(h.lim[wid][0]); body.append(h.lim[wid][1])
    pl = plo = 0
    pois = sorted(tuple(p) for p in h.pois.values())
    for la, lo, k, ms, dk, dd in pois:
        body.append(k)
        put_svarint(body, la - pl); put_svarint(body, lo - plo); pl, plo = la, lo
        body.append(ms)
        if a.format == 2:
            body.append(dk)
            body += struct.pack('>H', dd if dk else 0)
    comp = zlib.compress(bytes(body), 9)
    with open(a.dst, 'wb') as f:
        f.write(MAGIC[a.format])
        f.write(struct.pack('>iii', a.format, len(h.lim), len(pois)))
        f.write(comp)
    kinds = [sum(1 for p in pois if p[2] == k) for k in (1, 2, 3)]
    msg = (f'{a.dst}: UAREX00{a.format}; обмежень {len(h.lim)}, камер {kinds[0]}, переїздів {kinds[1]}, лежачих {kinds[2]}; '
           f'{len(comp) // 1024} КБ (без стиснення {len(body) // 1024} КБ)')
    if a.format == 2:
        ax = sum(1 for p in pois if p[2] == POI_CAMERA and p[4] == DIR_AXIS)
        tr = sum(1 for p in pois if p[2] == POI_CAMERA and p[4] == DIR_TRAVEL)
        msg += f'; камер з напрямком: вісь {ax}, рух {tr} (з них з відношень enforcement {n_rel}), без напрямку {kinds[0] - ax - tr}'
    print(msg)


if __name__ == '__main__':
    main()
