# Доповнення до доріг UAREX001

Окремий файл поруч з `ua-roads.bin` (UARDS001): обмеження швидкості за ідентифікатором дороги OSM і точкові
об'єкти. Створює `build_extras.py`, читає `verify_extras.py` (еталон для Swift-читача GNSS Nav iOS).
**`ua-roads.bin` не змінюється:** застосунок, якому доповнення не потрібні, їх не завантажує.
Багатобайтові числа — big-endian (як UARDS001). Координати — мікроградуси.

## Файл

| зсув | тип | значення |
|---|---|---|
| 0 | 8 байт | магія `UAREX001` |
| 8 | int32 | версія = 1 |
| 12 | int32 | nLimits — доріг з відомим обмеженням |
| 16 | int32 | nPois — точок |
| 20 | … | тіло, стиснуте **zlib** (з заголовком zlib) |

Тіло після розпакування:

```
nLimits × Limit      — за зростанням wayId
nPois   × Poi        — за зростанням широти
```

```
Limit:
  varint  dWay       wayId − попередній wayId (перший — від 0)
  u8      fwd        км/год у напрямку точок дороги (як у UARDS001); 0 — невідомо
  u8      bwd        км/год проти напрямку точок; 0 — невідомо
Poi:
  u8      kind       1 камера контролю швидкості, 2 залізничний переїзд (дорога × залізниця), 3 лежачий поліцейський
  svarint dLat       від попередньої точки (перша — від 0), мікроградуси
  svarint dLon
  u8      maxspeed   для камери — обмеження, якщо вказане; інакше 0
```

`varint` / `svarint` — як у UARDS001 (LEB128, zigzag).

## Звідки значення

- Обмеження: `maxspeed:forward` / `maxspeed:backward`, інакше `maxspeed`, інакше зона `maxspeed:type` чи
  `source:maxspeed` (UA:urban 50, UA:rural 90, UA:trunk 110, UA:motorway 130, UA:living_street 20). Невідоме не вигадуємо.
- Відрізки UARDS001 зберігають порядок точок дороги, тож `fwd` / `bwd` застосовні до них напряму за `wayId`.
- Камери: `highway=speed_camera` або `enforcement=maxspeed`; переїзди: лише `railway=level_crossing`
  (`railway=crossing` — пішохідний перехід через колію); лежачі: `traffic_calming=bump|hump|table|cushion|yes|dip|chicane`.

## Ліцензія даних
© OpenStreetMap contributors, ODbL 1.0 — як і UARDS001.
