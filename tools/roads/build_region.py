#!/usr/bin/env python3
"""
Збирання одного регіону для спільного roads.yml (22.10.2026). Повторює кроки колишніх roads.yml (Україна) і roads-il.yml
(Ізраїль) — ті самі скрипти, ті самі назви файлів — і додає країни (лише дороги, без доповнень iOS).

  python3 build_region.py --region '<JSON запису з REGIONS>' --src <витяг>.osm.pbf [--bbox minlat,minlon,maxlat,maxlon]
                          [--track true|false] [--tolerance 2] [--tile 0.025] [--warn-mb 300]

Звичайний режим: <cc>-roads.bin (+ .txt), за "extras" — <cc>-extras.bin і <cc>-extras2.bin (+ .txt), за "parts" — <part>-roads.bin
(і <part>-extras.bin, якщо в частини "extras"). Кожен *-roads.bin перевіряється (roads_index.check_container: заголовок,
≥ 1 МБ, ≤ межі застосунку 600 МБ, біля точки-проби є дорога). Понад --warn-mb — лише попередження (файл викладається).
Усе вдалося — у publish.txt перелік файлів для roads-latest; щось не так — publish.txt немає, код виходу ≠ 0.

Режим рамки (--bbox, лише регіон з "bbox_mode"): region-roads.bin, region-extras.bin, region-extras2.bin (+ .txt) — як колишній
roads.yml з рамкою; publish.txt не пишеться (у roads-latest рамка не йде).
"""
import argparse
import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from roads_index import APP_MAX_BYTES, MIN_BYTES, check_container  # noqa: E402

EXTRAS_FILTER = ['w/highway', 'n/highway=speed_camera', 'n/enforcement', 'r/enforcement',
                 'n/railway=level_crossing', 'n/traffic_calming']
PY = sys.executable


def run(cmd, txt=None):
    """Команда; з txt — вивід ще й у файл (як `| tee`). Помилка — виняток (крок падає)."""
    print('$ ' + ' '.join(cmd), flush=True)
    if txt is None:
        subprocess.run(cmd, check=True)
        return
    r = subprocess.run(cmd, check=True, stdout=subprocess.PIPE, text=True)
    sys.stdout.write(r.stdout)
    sys.stdout.flush()
    with open(txt, 'w', encoding='utf-8') as f:
        f.write(r.stdout)


def tool(name):
    return os.path.join(HERE, name)


def roads(src, out, args, bbox=None):
    cmd = [PY, tool('build_roads.py'), src, out] + args + (['--bbox', bbox] if bbox else [])
    run(cmd)
    run([PY, tool('verify_roads.py'), out], txt=out[:-4] + '.txt')


def extras(src, out, bbox=None, fmt2=False):
    cmd = [PY, tool('build_extras.py'), src, out] + (['--format', '2'] if fmt2 else []) + (['--bbox', bbox] if bbox else [])
    run(cmd)
    run([PY, tool('verify_extras.py'), out], txt=out[:-4] + '.txt')


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--region', required=True)
    ap.add_argument('--src', required=True)
    ap.add_argument('--bbox', default='')
    ap.add_argument('--track', default='true')
    ap.add_argument('--tolerance', default='2')
    ap.add_argument('--tile', default='0.025')
    ap.add_argument('--warn-mb', type=float, default=300)
    ap.add_argument('--max-bytes', type=int, default=APP_MAX_BYTES)
    ap.add_argument('--min-bytes', type=int, default=MIN_BYTES, help=argparse.SUPPRESS)   # лише для стенду
    ap.add_argument('--publish', default='publish.txt')
    a = ap.parse_args()

    r = json.loads(a.region)
    cc, parts = r['cc'], r.get('parts', [])
    args = ['--tolerance', a.tolerance or '2', '--tile', a.tile or '0.025']
    if a.track == 'false':
        args.append('--no-track')
    need_extras = bool(r.get('extras')) or any(p.get('extras') for p in parts)
    if os.path.exists(a.publish):
        os.remove(a.publish)

    run(['osmium', 'tags-filter', a.src, 'w/highway', '-o', 'roads-src.osm.pbf', '--overwrite'])
    if need_extras:
        # камери часто — окремі точки поза дорогою, тому фільтр ширший за w/highway (як у колишніх roads.yml / roads-il.yml)
        run(['osmium', 'tags-filter', a.src] + EXTRAS_FILTER + ['-o', 'extras-src.osm.pbf', '--overwrite'])

    if a.bbox:
        if not r.get('bbox_mode'):
            sys.exit(f'рамка дозволена лише для регіону з bbox_mode (не {cc})')
        if r.get('extras'):
            extras('extras-src.osm.pbf', 'region-extras.bin', bbox=a.bbox)
            extras('extras-src.osm.pbf', 'region-extras2.bin', bbox=a.bbox, fmt2=True)
        roads('roads-src.osm.pbf', 'region-roads.bin', args, bbox=a.bbox)
        print('рамка: зібрано region-*.bin (у roads-latest не йде)')
        return 0

    publish, bad = [], []

    def checked(path, probe):
        ok, msg = check_container(path, probe, a.max_bytes, a.min_bytes)
        print(msg if ok else f'::error::{msg}', flush=True)
        if not ok:
            bad.append(path)
            return
        mb = os.path.getsize(path) / 1e6
        if mb > a.warn_mb:
            print(f'::warning::{path} — {mb:.1f} МБ, більше за {a.warn_mb:.0f} МБ (викладається; межа застосунку — '
                  f'{a.max_bytes / 1048576:.0f} МБ)', flush=True)
        publish.extend([path, path[:-4] + '.txt'])

    if r.get('extras'):
        extras('extras-src.osm.pbf', f'{cc}-extras.bin')
        # UAREX002 — з напрямком камер (GNSS Nav iOS 0.9.3+); UAREX001 лишається для старих застосунків
        extras('extras-src.osm.pbf', f'{cc}-extras2.bin', fmt2=True)
    roads('roads-src.osm.pbf', f'{cc}-roads.bin', args)
    checked(f'{cc}-roads.bin', r['probe'])
    for p in parts:
        if p.get('extras'):
            extras('extras-src.osm.pbf', f"{p['cc']}-extras.bin", bbox=p['bbox'])
        roads('roads-src.osm.pbf', f"{p['cc']}-roads.bin", args, bbox=p['bbox'])
        checked(f"{p['cc']}-roads.bin", p.get('probe', r['probe']))

    if bad:
        print(f'::error::{cc}: не пройшли перевірку {bad} — у roads-latest нічого з цього регіону не йде')
        return 3
    # доповнення — у roads-latest разом із дорогами (і лише разом: iOS-маніфест посилається на всі три файли)
    if r.get('extras'):
        publish += [f'{cc}-extras.bin', f'{cc}-extras.txt', f'{cc}-extras2.bin', f'{cc}-extras2.txt']
    for p in parts:
        if p.get('extras'):
            publish += [f"{p['cc']}-extras.bin", f"{p['cc']}-extras.txt"]
    with open(a.publish, 'w', encoding='utf-8') as f:
        f.write('\n'.join(publish) + '\n')
    print('до roads-latest: ' + ' '.join(publish))
    return 0


if __name__ == '__main__':
    sys.exit(main())
