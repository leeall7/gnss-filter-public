#!/usr/bin/env python3
"""
OSM → доповнення до доріг (формат UAREX001, див. FORMAT_EXTRAS.md): обмеження швидкості за ідентифікатором
дороги OSM (у напрямку точок і проти) і точки — камери, залізничні переїзди, лежачі поліцейські.
Файл доріг ua-roads.bin (UARDS001) цей скрипт НЕ змінює: застосунок, якому доповнення не потрібні, їх просто
не завантажує.

Вхід — повний витяг або відфільтрований так (камери часто — окремі точки поза дорогою, тому w/highway мало):
    osmium tags-filter ukraine-latest.osm.pbf w/highway n/highway=speed_camera n/enforcement \\
        n/railway=level_crossing n/traffic_calming -o extras-src.osm.pbf
Використання:
    python3 build_extras.py extras-src.osm.pbf ua-extras.bin
    python3 build_extras.py extras-src.osm.pbf kyiv-extras.bin --bbox 49.3,29.2,51.6,32.2
Залежності: pip install osmium
"""
import argparse, struct, sys, zlib
import osmium

MAGIC = b'UAREX001'
# ті самі класи доріг, що й build_roads.py: обмеження лише для доріг, які є в UARDS001
CLASSES = {'motorway', 'trunk', 'primary', 'secondary', 'tertiary', 'unclassified', 'residential', 'living_street',
           'service', 'motorway_link', 'trunk_link', 'primary_link', 'secondary_link', 'tertiary_link', 'track'}
UA_ZONE = {'UA:urban': 50, 'UA:rural': 90, 'UA:motorway': 130, 'UA:trunk': 110, 'UA:living_street': 20}
POI_CAMERA, POI_RAIL, POI_BUMP = 1, 2, 3
CALMING = {'bump', 'hump', 'table', 'cushion', 'yes', 'dip', 'chicane'}


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


def put_varint(buf, v):
    while True:
        b = v & 0x7F
        v >>= 7
        if v: buf.append(b | 0x80)
        else:
            buf.append(b); return


def put_svarint(buf, v): put_varint(buf, (v << 1) ^ (v >> 63))


class H(osmium.SimpleHandler):
    def __init__(self, bbox):
        super().__init__()
        self.bbox = bbox
        self.lim = {}            # wayId → (fwd, bwd)
        self.pois = []           # (lat_udeg, lon_udeg, kind, maxspeed)

    def node(self, n):
        k = poi_kind(n.tags)
        if not k or not n.location.valid(): return
        la, lo = int(round(n.location.lat * 1e6)), int(round(n.location.lon * 1e6))
        if self.bbox and not (self.bbox[0] <= la <= self.bbox[2] and self.bbox[1] <= lo <= self.bbox[3]): return
        self.pois.append((la, lo, k, min(255, speed_of(n.tags.get('maxspeed')))))

    def way(self, w):
        t = w.tags
        if t.get('highway') not in CLASSES or t.get('area') == 'yes': return
        f, b = limits(t)
        if f or b: self.lim[w.id] = (min(255, f), min(255, b))


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('src'); ap.add_argument('dst')
    ap.add_argument('--bbox', default=None, help='minlat,minlon,maxlat,maxlon — точки лише в рамці (обмеження — усі)')
    a = ap.parse_args()
    bbox = None
    if a.bbox:
        v = [float(x) for x in a.bbox.split(',')]
        if len(v) != 4: sys.exit('--bbox: потрібно 4 числа')
        bbox = tuple(int(x * 1e6) for x in v)
    h = H(bbox)
    h.apply_file(a.src, locations=False)
    body = bytearray()
    prev = 0
    for wid in sorted(h.lim):
        put_varint(body, wid - prev); prev = wid
        body.append(h.lim[wid][0]); body.append(h.lim[wid][1])
    pl = plo = 0
    for la, lo, k, ms in sorted(h.pois):
        body.append(k)
        put_svarint(body, la - pl); put_svarint(body, lo - plo); pl, plo = la, lo
        body.append(ms)
    comp = zlib.compress(bytes(body), 9)
    with open(a.dst, 'wb') as f:
        f.write(MAGIC)
        f.write(struct.pack('>iii', 1, len(h.lim), len(h.pois)))
        f.write(comp)
    kinds = [sum(1 for p in h.pois if p[2] == k) for k in (1, 2, 3)]
    print(f'{a.dst}: обмежень {len(h.lim)}, камер {kinds[0]}, переїздів {kinds[1]}, лежачих {kinds[2]}; '
          f'{len(comp) // 1024} КБ (без стиснення {len(body) // 1024} КБ)')


if __name__ == '__main__':
    main()
