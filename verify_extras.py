#!/usr/bin/env python3
"""Еталонний читач UAREX001 / UAREX002 (для Swift-читача в GNSS Nav для iOS).
    python3 verify_extras.py ua-extras2.bin
    python3 verify_extras.py ua-extras2.bin --way 123456          # обмеження дороги
    python3 verify_extras.py ua-extras2.bin --near 50.4501,30.5234  # точки в радіусі 500 м
"""
import argparse, math, struct, sys, zlib

def get_varint(b, i):
    v = s = 0
    while True:
        x = b[i]; i += 1
        v |= (x & 0x7F) << s
        if x < 0x80: return v, i
        s += 7

def read(path):
    d = open(path, 'rb').read()
    magic = d[:8]
    if magic not in (b'UAREX001', b'UAREX002'): sys.exit('не UAREX001/UAREX002')
    ver, nl, npoi = struct.unpack('>iii', d[8:20])
    if (magic, ver) not in ((b'UAREX001', 1), (b'UAREX002', 2)): sys.exit(f'невідома версія {ver} для {magic.decode()}')
    b = zlib.decompress(d[20:])
    i = 0; wid = 0; lim = {}
    for _ in range(nl):
        dw, i = get_varint(b, i); wid += dw
        lim[wid] = (b[i], b[i + 1]); i += 2
    pois = []; la = lo = 0
    for _ in range(npoi):
        k = b[i]; i += 1
        if k not in (1, 2, 3): sys.exit(f'невідомий вид точки {k}')
        u, i = get_varint(b, i); la += (u >> 1) ^ -(u & 1)
        u, i = get_varint(b, i); lo += (u >> 1) ^ -(u & 1)
        if not (-90_000_000 <= la <= 90_000_000 and -180_000_000 <= lo <= 180_000_000): sys.exit('координати поза межами')
        ms = b[i]; i += 1
        dk, dd = 0, 0
        if ver == 2:
            dk = b[i]; dd = struct.unpack('>H', b[i + 1:i + 3])[0]; i += 3
            if dk not in (0, 1, 2) or dd >= 360 or (dk == 0 and dd != 0) or (dk and k != 1):
                sys.exit(f'зіпсований напрямок: вид {k}, напрям {dk}, {dd}°')
        pois.append((k, la / 1e6, lo / 1e6, ms, dk, dd))
    if i != len(b): sys.exit(f'зайві байти: {len(b) - i}')
    return ver, lim, pois

if __name__ == '__main__':
    ap = argparse.ArgumentParser(); ap.add_argument('src'); ap.add_argument('--way', type=int); ap.add_argument('--near')
    a = ap.parse_args()
    ver, lim, pois = read(a.src)
    names = {1: 'камера', 2: 'переїзд', 3: 'лежачий'}
    print(f'UAREX00{ver}: обмежень {len(lim)}; точок {len(pois)}: ' + ', '.join(f'{names[k]} {sum(1 for p in pois if p[0] == k)}' for k in names))
    if ver == 2:
        cams = [p for p in pois if p[0] == 1]
        ax = sum(1 for p in cams if p[4] == 1); tr = sum(1 for p in cams if p[4] == 2)
        print(f'камер із напрямком: вісь (куди дивиться) {ax}, напрямок руху {tr}, без напрямку {len(cams) - ax - tr}'
              + (f' — {100 * (ax + tr) / len(cams):.0f} % з напрямком' if cams else ''))
    if a.way is not None: print('дорога', a.way, '→ у напрямку точок / проти:', lim.get(a.way, 'невідомо'))
    if a.near:
        la, lo = map(float, a.near.split(','))
        dn = {0: '', 1: ' вісь %d°', 2: ' рух %d°'}
        for k, pla, plo, ms, dk, dd in pois:
            d = math.hypot((pla - la) * 111319.5, (plo - lo) * 111319.5 * math.cos(math.radians(la)))
            if d <= 500: print(f'  {names[k]:8} {pla:.6f},{plo:.6f}  {d:5.0f} м' + (f'  обмеження {ms}' if ms else '') + (dn[dk] % dd if dk else ''))
