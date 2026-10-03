# Дороги для прив'язки: збирання контейнера

Вихід — один файл `*.bin` формату UARDS001 (див. FORMAT.md): дороги для авто з
OpenStreetMap, порізані на плитки 0,1°, стиснуті. Уся Україна — орієнтовно
десятки МБ; область — одиниці МБ. Точну цифру дає перший прогін.

## Варіант А — GitHub Actions (нічого не ставити)

1. Покласти `tools/roads/` і `.github/workflows/roads.yml` у репозиторій.
2. GitHub → Actions → **Build road tiles** → *Run workflow*. Параметри:
   - `bbox` — порожньо = вся Україна; або `minlat,minlon,maxlat,maxlon`
     (Київська область приблизно `49.3,29.2,51.6,32.2`);
   - `track` — брати `highway=track` (польові/лісові) чи ні;
   - `tolerance` — спрощення геометрії, м (типово 2);
   - `tile` — розмір плитки, ° (типово 0.025: ~2,8 × 1,8 км; у центрі Києва 3×3 плитки —
     ~15 тис. відрізків і ~3 МБ пам'яті замість 100 тис. і 34 МБ при 0.1).
3. За 15–40 хвилин у розділі **Releases** з'явиться `roads-РРРР-ММ-ДД-N` з файлами
   `ua-roads.bin` (уся Україна), `kyiv-roads.bin` (Київщина, для тестів),
   `*.txt` зі зведенням. Ті самі файли є і в *Artifacts* запуску.
   Workflow також запускається сам першого числа кожного місяця.

Джерело даних — Geofabrik: <https://download.geofabrik.de/europe/ukraine-latest.osm.pbf>
(≈ 0,8–1 ГБ, оновлюється щодня; md5 поруч: `…pbf.md5`).

## Варіант Б — на ПК (Linux, WSL або macOS)

```bash
sudo apt install osmium-tool python3-pip          # macOS: brew install osmium-tool
pip install osmium numpy

wget https://download.geofabrik.de/europe/ukraine-latest.osm.pbf
wget https://download.geofabrik.de/europe/ukraine-latest.osm.pbf.md5 && md5sum -c ukraine-latest.osm.pbf.md5

# лишити лише дороги (у ~10 разів менше даних, далі все швидше)
osmium tags-filter ukraine-latest.osm.pbf w/highway -o ukraine-roads.osm.pbf

# уся Україна
python3 build_roads.py ukraine-roads.osm.pbf ua-roads.bin
# лише область / рамка
python3 build_roads.py ukraine-roads.osm.pbf kyiv-roads.bin --bbox 49.3,29.2,51.6,32.2
# інший розмір плитки (типово 0.025°)
python3 build_roads.py ukraine-roads.osm.pbf ua-roads.bin --tile 0.05
# без польових доріг, спрощення 3 м
python3 build_roads.py ukraine-roads.osm.pbf ua-roads.bin --no-track --tolerance 3

# перевірка
python3 verify_roads.py ua-roads.bin                          # зведення за класами
python3 verify_roads.py ua-roads.bin --near 50.4501,30.5234   # 5 найближчих доріг до точки
python3 verify_roads.py ua-roads.bin --kml 50.45,30.52 tile.kml   # плитка → KML (Google Earth)
```

Windows без WSL: `conda install -c conda-forge osmium-tool pyosmium numpy`, далі ті самі команди.

Пам'ять: крок `osmium tags-filter` — до 1 ГБ; `build_roads.py` на відфільтрованому
файлі — до 2 ГБ (індекс координат вузлів). Час на звичайному ПК — 5–15 хв.

## Доповнення для GNSS Nav (iOS)

Той самий запуск workflow збирає поруч `ua-extras.bin` / `kyiv-extras.bin` (формат UAREX001, див.
FORMAT_EXTRAS.md): обмеження швидкості за ідентифікатором дороги й камери, переїзди, лежачі — сотні КБ на всю
Україну. **`ua-roads.bin` не змінюється.** У `roads-latest` також кладеться `manifest.json` (розміри, SHA-256)
для завантаження в iOS. Android ці файли не читає.

```bash
osmium tags-filter ukraine-latest.osm.pbf w/highway n/highway=speed_camera n/enforcement \
    n/railway=level_crossing n/traffic_calming -o extras-src.osm.pbf
python3 build_extras.py extras-src.osm.pbf ua-extras.bin
python3 verify_extras.py ua-extras.bin --near 50.4501,30.5234
```

## Що далі

`verify_roads.py` — еталонний читач; Java-читач у застосунку повторює його
(RandomAccessFile → індекс → seek → Inflater → varint). Файл кладеться в
`Android/data/com.gnssfilter/files/roads/` — той самий каталог, що й логи та
ефемериди, видимий і доступний для ручного копіювання.
