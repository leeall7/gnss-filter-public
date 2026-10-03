#!/usr/bin/env python3
"""Еталонний читач UAREX001 (для Swift-читача в GNSS Nav для iOS).
    python3 verify_extras.py ua-extras.bin
    python3 verify_extras.py ua-extras.bin --way 123456          # обмеження дороги
    python3 verify_extras.py ua-extras.bin --near 50.4501,30.5234  # точки в радіусі 500 м
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
    if d[:8] != b'UAREX001': sys.exit('не UAREX001')
    ver, nl, npoi = struct.unpack('>iii', d[8:20])
    if ver != 1: sys.exit(f'невідома версія {ver}')
    b = zlib.decompress(d[20:])
    i = 0; wid = 0; lim = {}
    for _ in range(nl):
        dw, i = get_varint(b, i); wid += dw
        lim[wid] = (b[i], b[i + 1]); i += 2
    pois = []; la = lo = 0
    for _ in range(npoi):
        k = b[i]; i += 1
        u, i = get_varint(b, i); la += (u >> 1) ^ -(u & 1)
        u, i = get_varint(b, i); lo += (u >> 1) ^ -(u & 1)
        ms = b[i]; i += 1
        pois.append((k, la / 1e6, lo / 1e6, ms))
    if i != len(b): sys.exit(f'зайві байти: {len(b) - i}')
    return lim, pois

if __name__ == '__main__':
    ap = argparse.ArgumentParser(); ap.add_argument('src'); ap.add_argument('--way', type=int); ap.add_argument('--near')
    a = ap.parse_args()
    lim, pois = read(a.src)
    names = {1: 'камера', 2: 'переїзд', 3: 'лежачий'}
    print(f'обмежень {len(lim)}; точок {len(pois)}: ' + ', '.join(f'{names[k]} {sum(1 for p in pois if p[0] == k)}' for k in names))
    if a.way is not None: print('дорога', a.way, '→ у напрямку точок / проти:', lim.get(a.way, 'невідомо'))
    if a.near:
        la, lo = map(float, a.near.split(','))
        for k, pla, plo, ms in pois:
            d = math.hypot((pla - la) * 111319.5, (plo - lo) * 111319.5 * math.cos(math.radians(la)))
            if d <= 500: print(f'  {names[k]:8} {pla:.6f},{plo:.6f}  {d:5.0f} м' + (f'  обмеження {ms}' if ms else ''))
