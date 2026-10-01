#!/usr/bin/env python3
"""Модулі «Маршрути» і «Пошук» для GNSS Nav (iOS) — з OSM, на кожен регіон.

  roads    PBF → roads-<id>.sqlite: граф доріг для прив'язки (RoadMatch/RoadLearn) — відрізки між
           перехрестями з id вузлів, клас, односторонність, спрощена ламана. Фільтри й класи —
           ті самі, що в Android (tools/roads/build_roads.py, контейнер UARDS001), лише інший формат
           (SQLite вбудована в iOS; сітка 0,01° для «що поруч», індекс вузлів для зв'язності).
  search   PBF → search-<id>.sqlite: населені пункти, вулиці, адреси, об'єкти (FTS4, unicode61).
  valtiles плитки Valhalla всієї України → лише ті, що перетинають рамку регіону (без перебудови).
  manifest manifest.json для релізу routes-latest / search-latest.
Дані — ODbL, © OpenStreetMap contributors.
"""
import argparse, hashlib, json, math, os, shutil, sqlite3, struct, sys, datetime
from collections import defaultdict

# ------------------------------------------------------------------ дороги (як Android)
CLASSES = {
    'motorway': 0, 'trunk': 1, 'primary': 2, 'secondary': 3, 'tertiary': 4,
    'unclassified': 5, 'residential': 6, 'living_street': 7, 'service': 8,
    'motorway_link': 9, 'trunk_link': 10, 'primary_link': 11, 'secondary_link': 12, 'tertiary_link': 13,
    'track': 14,
}
SKIP_SERVICE = {'parking_aisle', 'drive-through', 'drive_through', 'emergency_access'}
CELL = 0.01           # сітка «що поруч», градуси

# Обмеження швидкості (як Android nav 11.4.0): число або зона UA:*; невідоме — 0 (знак не показуємо)
UA_ZONE = {'UA:urban': 50, 'UA:rural': 90, 'UA:motorway': 130, 'UA:trunk': 110, 'UA:living_street': 20}
# Точкові попередження: 1 — камера, 2 — залізничний переїзд, 3 — лежачий поліцейський
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


def limits(tags):
    """(у напрямку точок, проти) км/год; maxspeed:forward/backward мають перевагу."""
    base = speed_of(tags.get('maxspeed')) or UA_ZONE.get(tags.get('maxspeed:type', ''), 0) or UA_ZONE.get(tags.get('source:maxspeed', ''), 0)
    f = speed_of(tags.get('maxspeed:forward')) or base
    b = speed_of(tags.get('maxspeed:backward')) or base
    return f, b


def road_poi_kind(tags):
    if tags.get('highway') == 'speed_camera' or tags.get('enforcement') == 'maxspeed': return POI_CAMERA
    if tags.get('railway') in ('level_crossing', 'crossing'): return POI_RAIL
    if tags.get('traffic_calming') in CALMING: return POI_BUMP
    return 0


def wanted(tags):
    hw = tags.get('highway')
    if hw not in CLASSES or tags.get('area') == 'yes':
        return None
    if hw == 'service' and tags.get('service') in SKIP_SERVICE:
        return None
    return CLASSES[hw]


def oneway_of(tags):
    """0 — ні; 1 — у напрямку точок; 2 — проти. Кільця й motorway — односторонні без тегу."""
    ow = tags.get('oneway', '')
    if ow in ('yes', 'true', '1'): return 1
    if ow == '-1': return 2
    if ow in ('no', 'false', '0', 'reversible', 'alternating'): return 0
    if tags.get('junction') in ('roundabout', 'circular'): return 1
    if tags.get('highway') == 'motorway': return 1
    return 0


def simplify(pts, tol_m=2.0):
    """Дуглас–Пекер у метрах; кінці лишаються. pts — (lat_udeg, lon_udeg)."""
    if len(pts) <= 2: return pts
    cos = math.cos(math.radians(pts[0][0] / 1e6))
    ky, kx = 0.1113195, 0.1113195 * cos
    keep = [False] * len(pts); keep[0] = keep[-1] = True
    stack = [(0, len(pts) - 1)]
    while stack:
        a, b = stack.pop()
        if b - a < 2: continue
        ax, ay = pts[a][1] * kx, pts[a][0] * ky
        dx, dy = pts[b][1] * kx - ax, pts[b][0] * ky - ay
        L2 = dx * dx + dy * dy
        best, bi = -1.0, -1
        for i in range(a + 1, b):
            px, py = pts[i][1] * kx - ax, pts[i][0] * ky - ay
            t = max(0.0, min(1.0, (px * dx + py * dy) / L2)) if L2 > 0 else 0.0
            ex, ey = px - t * dx, py - t * dy
            d = ex * ex + ey * ey
            if d > best: best, bi = d, i
        if best > tol_m * tol_m:
            keep[bi] = True; stack += [(a, bi), (bi, b)]
    return [p for p, k in zip(pts, keep) if k]


def cell_of(lat, lon):
    return (math.floor(lat / CELL) + 9000) * 100000 + (math.floor(lon / CELL) + 18000)


def build_roads(pbf, out):
    import osmium
    count = defaultdict(int)

    class P1(osmium.SimpleHandler):
        def way(self, w):
            if wanted(w.tags) is None: return
            for n in w.nodes: count[n.ref] += 1

    P1().apply_file(pbf)
    junction = {k for k, v in count.items() if v >= 2}
    del count
    if os.path.exists(out): os.remove(out)
    db = sqlite3.connect(out)
    db.executescript("""
      PRAGMA journal_mode=OFF; PRAGMA synchronous=OFF;
      CREATE TABLE meta(k TEXT PRIMARY KEY, v TEXT);
      CREATE TABLE seg(id INTEGER PRIMARY KEY, way INTEGER, a INTEGER, b INTEGER, cls INTEGER, oneway INTEGER,
                       pts BLOB, minlat REAL, maxlat REAL, minlon REAL, maxlon REAL, maxfwd INTEGER, maxbwd INTEGER);
      CREATE TABLE cell(cell INTEGER, seg INTEGER);
      CREATE TABLE node(node INTEGER, seg INTEGER);
      CREATE TABLE poi(id INTEGER PRIMARY KEY, kind INTEGER, lat REAL, lon REAL, maxspeed INTEGER);
      CREATE TABLE poicell(cell INTEGER, poi INTEGER);
    """)
    stat_poi = [0, 0, 0, 0]
    stat = {'seg': 0, 'bbox': [90, 180, -90, -180]}

    class P2(osmium.SimpleHandler):
        def node(self, n):
            k = road_poi_kind(n.tags)
            if not k or not n.location.valid(): return
            la, lo = n.location.lat, n.location.lon
            cur = db.execute('INSERT INTO poi(kind,lat,lon,maxspeed) VALUES(?,?,?,?)', (k, la, lo, speed_of(n.tags.get('maxspeed'))))
            db.execute('INSERT INTO poicell VALUES(?,?)', (cell_of(la, lo), cur.lastrowid))
            stat_poi[k] += 1

        def way(self, w):
            cls = wanted(w.tags)
            if cls is None: return
            ow = oneway_of(w.tags)
            self.lim = limits(w.tags)
            pts, refs = [], []
            for n in w.nodes:
                if not n.location.valid():
                    self.emit(w.id, cls, ow, pts, refs); pts, refs = [], []; continue
                pts.append((int(round(n.location.lat * 1e6)), int(round(n.location.lon * 1e6))))
                refs.append(n.ref)
            self.emit(w.id, cls, ow, pts, refs)

        def emit(self, wid, cls, ow, pts, refs):
            if len(pts) < 2: return
            cut = [0] + [i for i in range(1, len(refs) - 1) if refs[i] in junction] + [len(refs) - 1]
            for a, b in zip(cut, cut[1:]):
                self.seg(wid, cls, ow, simplify(pts[a:b + 1]), refs[a], refs[b])

        def seg(self, wid, cls, ow, pts, na, nb):
            lats = [p[0] / 1e6 for p in pts]; lons = [p[1] / 1e6 for p in pts]
            blob = b''.join(struct.pack('<ii', p[0], p[1]) for p in pts)
            cur = db.execute('INSERT INTO seg(way,a,b,cls,oneway,pts,minlat,maxlat,minlon,maxlon,maxfwd,maxbwd) VALUES(?,?,?,?,?,?,?,?,?,?,?,?)',
                             (wid, na, nb, cls, ow, blob, min(lats), max(lats), min(lons), max(lons), self.lim[0], self.lim[1]))
            sid = cur.lastrowid
            cells = {cell_of(la, lo) for la, lo in zip(lats, lons)}
            # довгі прямі відрізки — ще й клітинки між точками (кожні ~500 м)
            for i in range(len(pts) - 1):
                la0, lo0, la1, lo1 = lats[i], lons[i], lats[i + 1], lons[i + 1]
                n = int(max(abs(la1 - la0), abs(lo1 - lo0)) / (CELL / 2))
                for k in range(1, n + 1):
                    t = k / (n + 1); cells.add(cell_of(la0 + t * (la1 - la0), lo0 + t * (lo1 - lo0)))
            db.executemany('INSERT INTO cell VALUES(?,?)', [(c, sid) for c in cells])
            db.executemany('INSERT INTO node VALUES(?,?)', [(na, sid)] + ([(nb, sid)] if nb != na else []))
            stat['seg'] += 1
            bb = stat['bbox']
            bb[0] = min(bb[0], min(lats)); bb[1] = min(bb[1], min(lons)); bb[2] = max(bb[2], max(lats)); bb[3] = max(bb[3], max(lons))

    P2().apply_file(pbf, locations=True)
    db.executescript('CREATE INDEX cell_i ON cell(cell); CREATE INDEX node_i ON node(node); CREATE INDEX poicell_i ON poicell(cell);')
    bb = stat['bbox']
    db.executemany('INSERT INTO meta VALUES(?,?)', [('format', 'gnss-roads-2'), ('cell_deg', str(CELL)),
                   ('poi', f'камер {stat_poi[1]}, переїздів {stat_poi[2]}, лежачих {stat_poi[3]}'),
                   ('bbox', ','.join(f'{x:.5f}' for x in bb)), ('segments', str(stat['seg']))])
    db.commit(); db.execute('VACUUM'); db.close()
    print(f'дороги: {stat["seg"]} відрізків, перехресть {len(junction)}, камер {stat_poi[1]}, переїздів {stat_poi[2]}, лежачих {stat_poi[3]} → {out} ({os.path.getsize(out)//1024} КБ)')


# ------------------------------------------------------------------ пошук
PLACE_RANK = {'city': 100, 'town': 80, 'village': 50, 'suburb': 45, 'hamlet': 35, 'neighbourhood': 30, 'quarter': 30}
POI_KEYS = ('amenity', 'shop', 'tourism', 'leisure', 'office', 'healthcare', 'railway', 'aeroway')
KIND_PLACE, KIND_VILLAGE, KIND_STREET, KIND_ADDR, KIND_POI = 0, 1, 2, 3, 4


def uk_name(tags):
    return tags.get('name:uk') or tags.get('name')


def build_search(pbf, out):
    import osmium
    places, streets, addrs, pois = [], {}, [], []

    def centroid(w):
        la = lo = 0.0; n = 0
        for nd in w.nodes:
            if nd.location.valid(): la += nd.location.lat; lo += nd.location.lon; n += 1
        return (la / n, lo / n) if n else None

    class H(osmium.SimpleHandler):
        def node(self, n):
            t = n.tags
            if not n.location.valid(): return
            la, lo = n.location.lat, n.location.lon
            nm = uk_name(t)
            if nm and t.get('place') in PLACE_RANK:
                pop = t.get('population', '').replace(' ', '')
                bonus = int(min(20, 4 * math.log10(int(pop)))) if pop.isdigit() and int(pop) > 0 else 0
                places.append((nm, t.get('place'), la, lo, PLACE_RANK[t.get('place')] + bonus))
            # заклад з власною адресою — і заклад, і адреса
            if nm and any(k in t for k in POI_KEYS):
                pois.append((nm, poi_kind(t), la, lo, own_addr(t)))
            if t.get('addr:housenumber') and t.get('addr:street'):
                addrs.append((t.get('addr:street'), t.get('addr:housenumber'), t.get('addr:city'), la, lo))

        def way(self, w):
            t = w.tags
            nm = uk_name(t)
            if nm and t.get('highway') in CLASSES:
                c = centroid(w)
                if c:
                    n = len(w.nodes)
                    key = nm
                    streets.setdefault(key, []).append((c[0], c[1], n))
                return
            is_poi = nm and any(k in t for k in POI_KEYS)
            has_addr = t.get('addr:housenumber') and t.get('addr:street')
            if is_poi or has_addr:
                c = centroid(w)
                if c and is_poi: pois.append((nm, poi_kind(t), c[0], c[1], own_addr(t)))
                if c and has_addr: addrs.append((t.get('addr:street'), t.get('addr:housenumber'), t.get('addr:city'), c[0], c[1]))

    H().apply_file(pbf, locations=True)

    # найближчий населений пункт — сітка 0,1°
    grid = defaultdict(list)
    for p in places:
        if p[1] in ('city', 'town', 'village', 'hamlet'): grid[(int(p[2] * 10), int(p[3] * 10))].append(p)

    def nearest_place(la, lo):
        best, bd = None, 1e18
        gi, gj = int(la * 10), int(lo * 10)
        for di in (-1, 0, 1):
            for dj in (-1, 0, 1):
                for p in grid.get((gi + di, gj + dj), ()):
                    d = (p[2] - la) ** 2 + ((p[3] - lo) * math.cos(math.radians(la))) ** 2
                    # місто «притягує» далі за село
                    d /= (1 + p[4] / 50.0)
                    if d < bd: bd, best = d, p
        return best[0] if best else ''

    if os.path.exists(out): os.remove(out)
    db = sqlite3.connect(out)
    db.executescript("""
      PRAGMA journal_mode=OFF; PRAGMA synchronous=OFF;
      CREATE TABLE meta(k TEXT PRIMARY KEY, v TEXT);
      CREATE TABLE item(id INTEGER PRIMARY KEY, kind INTEGER, name TEXT, extra TEXT, lat REAL, lon REAL, rank INTEGER);
      CREATE VIRTUAL TABLE fts USING fts4(name, extra, tokenize=unicode61);
    """)
    rows = []
    for nm, pl, la, lo, rk in places:
        rows.append((KIND_PLACE if pl in ('city', 'town') else KIND_VILLAGE, nm, '', la, lo, rk))
    # вулиці: однакова назва в різних населених пунктах — окремі записи; в одному — одна (найдовша частина)
    for nm, parts in streets.items():
        by_place = {}
        for la, lo, n in parts:
            pl = nearest_place(la, lo)
            if pl not in by_place or by_place[pl][2] < n: by_place[pl] = (la, lo, n)
        for pl, (la, lo, n) in by_place.items():
            rows.append((KIND_STREET, nm, pl, la, lo, 30))
    for st, hn, city, la, lo in addrs:
        rows.append((KIND_ADDR, f'{st}, {hn}', city or nearest_place(la, lo), la, lo, 10))
    # адреса закладу: власні теги, інакше — найближча адреса в межах 60 м (сітка ~100 м)
    agrid = defaultdict(list)
    for st, hn, city, la, lo in addrs: agrid[(int(la * 1000), int(lo * 1000))].append((la, lo, f'{st}, {hn}'))

    def nearest_addr(la, lo):
        best, bd = '', 60.0
        gi, gj = int(la * 1000), int(lo * 1000)
        k = math.cos(math.radians(la))
        for di in (-1, 0, 1):
            for dj in (-1, 0, 1):
                for a_la, a_lo, txt in agrid.get((gi + di, gj + dj), ()):
                    d = math.hypot((a_la - la) * 111320, (a_lo - lo) * 111320 * k)
                    if d < bd: bd, best = d, txt
        return best

    with_addr = 0
    for nm, kind, la, lo, adr in pois:
        pl = nearest_place(la, lo)
        adr = adr or nearest_addr(la, lo)
        if adr: with_addr += 1
        rows.append((KIND_POI, nm, ' · '.join(x for x in (kind, adr, pl) if x), la, lo, 20))
    db.executemany('INSERT INTO item(kind,name,extra,lat,lon,rank) VALUES(?,?,?,?,?,?)', rows)
    db.execute('INSERT INTO fts(docid,name,extra) SELECT id,name,extra FROM item')
    db.execute('CREATE INDEX item_ll ON item(lat, lon)')
    db.executemany('INSERT INTO meta VALUES(?,?)', [('format', 'gnss-search-1'), ('items', str(len(rows)))])
    db.commit(); db.execute("INSERT INTO fts(fts) VALUES('optimize')"); db.commit(); db.execute('VACUUM'); db.close()
    print(f'пошук: пунктів {len(places)}, вулиць {len(streets)}, адрес {len(addrs)}, об\'єктів {len(pois)} (з адресою {with_addr}) → {out} ({os.path.getsize(out)//1024} КБ)')


POI_UK = {'fuel': 'АЗС', 'hospital': 'лікарня', 'pharmacy': 'аптека', 'police': 'поліція', 'cafe': 'кафе',
          'restaurant': 'ресторан', 'school': 'школа', 'bank': 'банк', 'atm': 'банкомат', 'parking': 'стоянка',
          'supermarket': 'супермаркет', 'hotel': 'готель', 'station': 'вокзал', 'townhall': 'рада',
          'post_office': 'пошта', 'car_repair': 'СТО', 'marketplace': 'ринок', 'clinic': 'клініка'}


def own_addr(t):
    st, hn = t.get('addr:street'), t.get('addr:housenumber')
    return f'{st}, {hn}' if st and hn else ''


def poi_kind(t):
    for k in POI_KEYS:
        v = t.get(k)
        if v: return POI_UK.get(v, v.replace('_', ' '))
    return ''


# ------------------------------------------------------------------ плитки Valhalla
LEVEL_DEG = {0: 4.0, 1: 1.0, 2: 0.25}


def valtiles(src, dst, bbox, margin=0.25):
    """Копіює з tile_dir лише плитки, що перетинають рамку [w,s,e,n] (+запас). Шлях плитки → id → ряд/стовпець."""
    w, s, e, n = bbox[0] - margin, bbox[1] - margin, bbox[2] + margin, bbox[3] + margin
    kept = total = 0
    for level, size in LEVEL_DEG.items():
        root = os.path.join(src, str(level))
        if not os.path.isdir(root): continue
        ncols = int(round(360 / size))
        for dp, _, fns in os.walk(root):
            for fn in fns:
                if not fn.endswith('.gph'): continue
                total += 1
                rel = os.path.relpath(os.path.join(dp, fn), root)
                tid = int(rel.replace(os.sep, '').replace('.gph', ''))
                row, col = divmod(tid, ncols)
                la0, lo0 = -90 + row * size, -180 + col * size
                if la0 + size < s or la0 > n or lo0 + size < w or lo0 > e: continue
                out = os.path.join(dst, str(level), rel)
                os.makedirs(os.path.dirname(out), exist_ok=True)
                shutil.copy2(os.path.join(dp, fn), out)
                kept += 1
    print(f'плитки Valhalla: {kept} з {total}')
    if kept == 0: sys.exit('жодної плитки для рамки ' + str(bbox))


# ------------------------------------------------------------------ маніфест
def sha256(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for chunk in iter(lambda: f.read(8 << 20), b''): h.update(chunk)
    return h.hexdigest()


def manifest(work, module, pattern, regions_json, osm_date):
    meta = json.load(open(regions_json, encoding='utf-8'))
    regs = []
    for rid in ['UA'] + sorted(k for k in meta if k != 'UA'):
        files = []
        for pat in pattern.split(','):
            fn = pat.replace('{id}', rid)
            p = os.path.join(work, fn)
            if not os.path.isfile(p): sys.exit('немає ' + p)
            files.append({'file': fn, 'size': os.path.getsize(p), 'sha256': sha256(p)})
        regs.append({'id': rid, 'name': meta[rid]['name'], 'bbox': meta[rid]['bbox'], 'files': files})
    now = datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
    m = {'schema': 1, 'module': module, 'generated': now, 'osm_date': osm_date,
         'license': 'ODbL 1.0 — © OpenStreetMap contributors', 'regions': regs}
    out = os.path.join(work, f'manifest-{module}.json')
    json.dump(m, open(out, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print(f'{module}: {len(regs)} регіонів, {sum(f["size"] for r in regs for f in r["files"]) / 1e6:.0f} МБ')


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('step', choices=['roads', 'search', 'valtiles', 'manifest'])
    ap.add_argument('--pbf'); ap.add_argument('--out')
    ap.add_argument('--src'); ap.add_argument('--dst'); ap.add_argument('--bbox')
    ap.add_argument('--work', default='work'); ap.add_argument('--module'); ap.add_argument('--pattern')
    ap.add_argument('--regions'); ap.add_argument('--osm-date', default='')
    a = ap.parse_args()
    if a.step == 'roads': build_roads(a.pbf, a.out)
    elif a.step == 'search': build_search(a.pbf, a.out)
    elif a.step == 'valtiles': valtiles(a.src, a.dst, [float(x) for x in a.bbox.split(',')])
    else: manifest(a.work, a.module, a.pattern, a.regions, a.osm_date)
