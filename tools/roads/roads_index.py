#!/usr/bin/env python3
"""
Списки мап доріг у релізі roads-latest — для спільного roads.yml (22.10.2026, план PLAN_ROADS_COUNTRIES_ANDROID).

  check  — перевірити контейнер (заголовок UARDS001, ≥ 1 МБ, ≤ межі застосунку, біля --probe дорога ≤ 300 м):
           python3 roads_index.py check lt-roads.bin --probe 54.6872,25.2797

  merge  — roads-index.json для GNSS Filter (Android): усі *-roads.bin, що СПРАВДІ лежать у релізі:
           python3 roads_index.py merge --assets release.json --headers hdr/ --regions regions.json \
                   [--old old-index.json] --out roads-index.json

  ios    — manifest.json для GNSS Nav (iOS) — ТОЙ САМИЙ формат, що писали roads.yml / roads-il.yml (schema 1, module roads,
           регіони UA і IL, файли <cc>-roads.bin, <cc>-extras.bin, <cc>-extras2.bin). Регіон оновлюється лише тоді, коли його
           <cc>-roads.bin викладено в цьому запуску (updated_at ≥ --since); інакше старий запис лишається як є. Нічого не
           змінилось — код 10, маніфест не викладати (новий «generated» без нових файлів iOS сприйняв би як оновлення):
           python3 roads_index.py ios --assets release.json --regions regions.json --old manifest-old.json \
                   --since 2026-10-23T03:17:00Z --out manifest.json

release.json — `gh api repos/<repo>/releases/tags/roads-latest` (assets: name, size, updated_at, digest «sha256:…»);
hdr/<name>.hdr — перші 32 байти кожного *-roads.bin (HTTP Range); regions.json — список REGIONS з roads.yml.

Формат roads-index.json (format 1):
  { "format": 1, "generated": "…Z",
    "maps": [ { "name": "lt-roads.bin", "cc": "LT", "full": true,
                "label": {"uk": "Литва", "en": "Lithuania", "he": "ליטא"},
                "bytes": 31457280, "bbox": [53.875, 56.475, 20.9, 26.85],   # південь, північ, захід, схід (як RoadCheck.BOX)
                "built": "2026-10-23", "sha256": "…" }, … ] }
"""
import argparse
import datetime as dt
import hashlib
import json
import math
import os
import struct
import subprocess
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from verify_roads import Roads, dist_to_segment  # noqa: E402  еталонний читач формату

MAGIC = b'UARDS001'
MIN_BYTES = 1024 * 1024                    # RoadFetch.MIN_BYTES
APP_MAX_BYTES = 600 * 1024 * 1024          # RoadFetch.MAX_BYTES — більший файл застосунок відкине («файл завеликий»)
PROBE_MAX_M = 300.0
NOTHING_CHANGED = 10


def now_utc():
    return dt.datetime.now(dt.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')


def parse_header(b):
    """32 байти заголовка → (bbox [s, n, w, e] у градусах, tile) або None."""
    if len(b) < 32 or b[:8] != MAGIC:
        return None
    ver, tile, lat0, lon0, n_lat, n_lon = struct.unpack('>iiiiii', b[8:32])
    if ver != 1 or tile <= 0 or n_lat <= 0 or n_lon <= 0:
        return None
    s, w = lat0 / 1e6, lon0 / 1e6
    n, e = (lat0 + n_lat * tile) / 1e6, (lon0 + n_lon * tile) / 1e6
    if not (-90 <= s < n <= 90 and -180 <= w < e <= 180):
        return None
    return [round(s, 6), round(n, 6), round(w, 6), round(e, 6)], tile


def sha256_of(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for chunk in iter(lambda: f.read(1 << 20), b''):
            h.update(chunk)
    return h.hexdigest()


def check_container(path, probe, max_bytes=APP_MAX_BYTES, min_bytes=MIN_BYTES):
    """(True, опис) — придатний; (False, причина) — ні."""
    size = os.path.getsize(path)
    with open(path, 'rb') as f:
        hdr = parse_header(f.read(32))
    if hdr is None:
        return False, f'{path}: не контейнер UARDS001 або хибний заголовок'
    if size < min_bytes:
        return False, f'{path}: {size} Б — замалий (< {min_bytes} Б), застосунок такий не прийме'
    if size > max_bytes:
        return False, f'{path}: {size / 1e6:.1f} МБ — більший за межу застосунку {max_bytes / 1048576:.0f} МБ'
    bbox = hdr[0]
    lat, lon = map(float, probe.split(','))
    if not (bbox[0] <= lat <= bbox[1] and bbox[2] <= lon <= bbox[3]):
        return False, f'{path}: точка-проба {lat},{lon} поза рамкою {bbox}'
    best = math.inf
    for s in Roads(path).around(lat, lon):
        best = min(best, dist_to_segment(lat, lon, s['pts'])[0])
    if best > PROBE_MAX_M:
        return False, f'{path}: найближча дорога до {lat},{lon} — {best:.0f} м (> {PROBE_MAX_M:.0f})'
    return True, f'{path}: {size / 1e6:.1f} МБ, рамка {bbox}, проба {best:.0f} м — придатний'


def load_json(path, default):
    if not path or not os.path.exists(path):
        return default
    try:
        with open(path, encoding='utf-8') as f:
            return json.load(f)
    except (OSError, ValueError) as e:
        print(f'увага: {path} не читається ({e}) — ігнорую', file=sys.stderr)
        return default


def load_assets(path):
    rel = load_json(path, None)
    if rel is None:
        raise SystemExit(f'немає {path}')
    items = rel.get('assets', []) if isinstance(rel, dict) else rel
    return {x['name']: x for x in items}


def region_files(regions):
    """Назва *-roads.bin → {cc, full, label, order} з REGIONS (основний файл і частини)."""
    out, k = {}, 0
    for r in regions:
        cc = r.get('country', r['cc']).upper()
        out[r['cc'] + '-roads.bin'] = {'cc': cc, 'full': True, 'label': r['label'], 'order': k}
        k += 1
        for p in r.get('parts', []):
            out[p['cc'] + '-roads.bin'] = {'cc': cc, 'full': False, 'label': p['label'], 'order': k}
            k += 1
    return out


def cmd_check(a):
    ok, msg = check_container(a.bin, a.probe, a.max_bytes)
    print(msg, file=sys.stdout if ok else sys.stderr)
    return 0 if ok else 3


def cmd_merge(a):
    assets = load_assets(a.assets)
    known = region_files(load_json(a.regions, []))
    old = {m['name']: m for m in load_json(a.old, {}).get('maps', []) if isinstance(m, dict) and 'name' in m}
    out = []
    for name in sorted(n for n in assets if n.endswith('-roads.bin')):
        asset = assets[name]
        hdr = None
        hp = os.path.join(a.headers, name + '.hdr')
        if os.path.exists(hp):
            with open(hp, 'rb') as f:
                hdr = parse_header(f.read(32))
        if hdr is None:
            print(f'увага: {name} — заголовок не прочитано, в індекс не беру', file=sys.stderr)
            continue
        base = known.get(name) or old.get(name)
        if base is None:
            print(f'увага: {name} — немає в REGIONS і в старому індексі, в індекс не беру', file=sys.stderr)
            continue
        e = {'name': name, 'cc': base.get('cc', ''), 'full': bool(base.get('full', True)), 'label': base.get('label', {}),
             'bytes': int(asset.get('size', 0)), 'bbox': hdr[0], 'built': (asset.get('updated_at') or '')[:10]}
        dg = asset.get('digest') or ''
        if dg.startswith('sha256:'):
            e['sha256'] = dg[7:]
        elif name in old and old[name].get('bytes') == e['bytes'] and old[name].get('sha256'):
            e['sha256'] = old[name]['sha256']
        e['_order'] = known[name]['order'] if name in known else 10_000
        out.append(e)
    out.sort(key=lambda m: (m['_order'], m['label'].get('en', m['name'])))
    for m in out:
        del m['_order']
    if not out:
        print('порожній індекс — не записую', file=sys.stderr)
        return 3
    with open(a.out, 'w', encoding='utf-8') as f:
        json.dump({'format': 1, 'generated': now_utc(), 'maps': out}, f, ensure_ascii=False, indent=1)
    for m in out:
        print(f"  {m['name']:16s} {m['bytes'] / 1e6:7.1f} МБ  {m['built']}  {m['label'].get('uk', '')}")
    print(f'записано {a.out}: мап {len(out)}')
    return 0


def asset_sha(name, asset, repo, tag):
    """sha256 файла в релізі: digest GitHub (рахує сам GitHub) → інакше завантажити й порахувати."""
    dg = asset.get('digest') or ''
    if dg.startswith('sha256:'):
        return dg[7:]
    if not repo:
        raise SystemExit(f'{name}: немає digest і не задано --repo — не можу порахувати sha256')
    with tempfile.TemporaryDirectory() as d:
        subprocess.run(['gh', 'release', 'download', tag, '-R', repo, '-p', name, '-D', d], check=True)
        return sha256_of(os.path.join(d, name))


def cmd_ios(a):
    assets = load_assets(a.assets)
    regions = load_json(a.regions, [])
    old = load_json(a.old, {'regions': []})
    old_regs = [r for r in old.get('regions', []) if isinstance(r, dict) and 'id' in r]
    replaced = {}
    for r in regions:
        ios = r.get('ios')
        if not ios:
            continue
        names = [r['cc'] + '-roads.bin', r['cc'] + '-extras.bin', r['cc'] + '-extras2.bin']
        main = assets.get(names[0])
        if main is None or (main.get('updated_at') or '') < a.since:
            continue                                # цей регіон у запуску не перезбирався — запис лишається старим
        if any(n not in assets for n in names):
            print(f'увага: {ios["id"]} — у релізі бракує {[n for n in names if n not in assets]}; запис не змінюю',
                  file=sys.stderr)
            continue
        files = [{'file': n, 'size': int(assets[n]['size']), 'sha256': asset_sha(n, assets[n], a.repo, a.tag)}
                 for n in names]
        replaced[ios['id']] = {'id': ios['id'], 'name': ios['name'], 'bbox': ios['bbox'], 'files': files}
    if not replaced:
        print('iOS: жоден регіон (UA / IL) у цьому запуску не перезбирався — manifest.json не змінюю')
        return NOTHING_CHANGED
    regs = [r for r in old_regs if r['id'] not in replaced] + list(replaced.values())
    m = {'schema': 1, 'module': 'roads', 'generated': now_utc(),
         'license': 'ODbL 1.0 — © OpenStreetMap contributors', 'regions': sorted(regs, key=lambda r: r['id'])}
    with open(a.out, 'w', encoding='utf-8') as f:
        json.dump(m, f, ensure_ascii=False, indent=1)
    print('iOS: оновлено ' + ', '.join(sorted(replaced)) + '; ' + json.dumps(m, ensure_ascii=False)[:400])
    return 0


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest='cmd', required=True)
    c = sub.add_parser('check')
    c.add_argument('bin')
    c.add_argument('--probe', required=True)
    c.add_argument('--max-bytes', type=int, default=APP_MAX_BYTES)
    g = sub.add_parser('merge')
    g.add_argument('--assets', required=True)
    g.add_argument('--headers', required=True)
    g.add_argument('--regions', required=True)
    g.add_argument('--old')
    g.add_argument('--out', required=True)
    i = sub.add_parser('ios')
    i.add_argument('--assets', required=True)
    i.add_argument('--regions', required=True)
    i.add_argument('--old')
    i.add_argument('--since', required=True)
    i.add_argument('--repo')
    i.add_argument('--tag', default='roads-latest')
    i.add_argument('--out', required=True)
    a = ap.parse_args()
    return {'check': cmd_check, 'merge': cmd_merge, 'ios': cmd_ios}[a.cmd](a)


if __name__ == '__main__':
    sys.exit(main())
