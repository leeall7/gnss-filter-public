#!/usr/bin/env python3
"""Офлайн-мапи для GNSS Nav (iOS): Україна + кожна область, PMTiles схеми Protomaps v4.

Кроки (усе — у робочій теці --work):
  regions  — межі областей з OSM (osmium export, admin_level=4, ISO3166-2 UA-*) → regions/*.geojson
  extract  — pmtiles extract: Україна з планетарної збірки, області — з українського файла
  assets   — шрифти Noto Sans (кирилиця) і значки з protomaps/basemaps-assets → map-assets.tar (ustar)
  manifest — manifest.json: розмір, sha256, рамка, назва; схема, дата даних
Ліцензія даних — ODbL (© OpenStreetMap contributors); плитки — Protomaps Basemap (ODbL Produced Work).
"""
import argparse, hashlib, json, os, subprocess, sys, tarfile, datetime

FONTS = {"Noto Sans Regular": "NotoSans-Regular", "Noto Sans Medium": "NotoSans-Medium", "Noto Sans Italic": "NotoSans-Italic"}
SPRITES = ["light", "dark"]


def sh(*cmd):
    print("+", " ".join(cmd), flush=True)
    subprocess.run(cmd, check=True)


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def bbox_of(geom):
    xs, ys = [], []
    def walk(c):
        if isinstance(c[0], (int, float)):
            xs.append(c[0]); ys.append(c[1])
        else:
            for x in c: walk(x)
    walk(geom["coordinates"])
    return [round(min(xs), 4), round(min(ys), 4), round(max(xs), 4), round(max(ys), 4)]


def regions(work, adm_geojsonseq):
    """Області й уся країна з osmium export (GeoJSON Text Sequence)."""
    out = os.path.join(work, "regions"); os.makedirs(out, exist_ok=True)
    found = {}
    with open(adm_geojsonseq, encoding="utf-8") as f:
        for line in f:
            line = line.strip().lstrip("\x1e")
            if not line: continue
            ft = json.loads(line)
            p = ft.get("properties", {})
            if ft.get("geometry", {}).get("type") not in ("Polygon", "MultiPolygon"): continue
            lvl, iso = str(p.get("admin_level", "")), p.get("ISO3166-2", "")
            if lvl == "2" and p.get("ISO3166-1", p.get("ISO3166-1:alpha2", "")) == "UA":
                rid = "UA"
            elif lvl == "4" and iso.startswith("UA-"):
                rid = iso
            else:
                continue
            name = p.get("name:uk") or p.get("name") or rid
            if rid == "UA": name = "Уся Україна"
            # кілька частин однієї області — лишаємо більшу за рамкою
            bb = bbox_of(ft["geometry"])
            area = (bb[2] - bb[0]) * (bb[3] - bb[1])
            if rid in found and found[rid]["area"] >= area: continue
            found[rid] = {"name": name, "bbox": bb, "area": area}
            with open(os.path.join(out, rid + ".geojson"), "w", encoding="utf-8") as g:
                json.dump({"type": "FeatureCollection", "features": [{"type": "Feature", "properties": {"id": rid},
                           "geometry": ft["geometry"]}]}, g, ensure_ascii=False)
    meta = {k: {"name": v["name"], "bbox": v["bbox"]} for k, v in sorted(found.items())}
    with open(os.path.join(work, "regions.json"), "w", encoding="utf-8") as g:
        json.dump(meta, g, ensure_ascii=False, indent=1)
    print(f"областей: {len([k for k in meta if k != 'UA'])}, країна: {'UA' in meta}")
    if "UA" not in meta or len(meta) < 20:
        sys.exit("замало регіонів — перевірте межі OSM")
    return meta


def extract(work, planet, pmtiles_bin, maxzoom):
    meta = json.load(open(os.path.join(work, "regions.json"), encoding="utf-8"))
    ua = os.path.join(work, "map-UA.pmtiles")
    sh(pmtiles_bin, "extract", planet, ua, "--region=" + os.path.join(work, "regions", "UA.geojson"),
       "--maxzoom=" + str(maxzoom), "--download-threads=8")
    for rid in meta:
        if rid == "UA": continue
        sh(pmtiles_bin, "extract", ua, os.path.join(work, f"map-{rid}.pmtiles"),
           "--region=" + os.path.join(work, "regions", rid + ".geojson"))


def assets(work, assets_repo):
    """ustar без стиснення: iPhone розпаковує власним простим читачем (без сторонніх бібліотек)."""
    tar_path = os.path.join(work, "map-assets.tar")
    with tarfile.open(tar_path, "w", format=tarfile.USTAR_FORMAT) as t:
        for src, dst in FONTS.items():
            d = os.path.join(assets_repo, "fonts", src)
            if not os.path.isdir(d): sys.exit("немає шрифту " + d)
            for fn in sorted(os.listdir(d)):
                if fn.endswith(".pbf"): t.add(os.path.join(d, fn), arcname=f"fonts/{dst}/{fn}")
        lic = os.path.join(assets_repo, "fonts", "OFL.txt")
        if os.path.isfile(lic): t.add(lic, arcname="fonts/OFL.txt")
        sp = os.path.join(assets_repo, "sprites", "v4")
        for name in SPRITES:
            for suf in ("", "@2x"):
                for ext in (".json", ".png"):
                    fn = os.path.join(sp, name + suf + ext)
                    if not os.path.isfile(fn): sys.exit("немає значків " + fn)
                    t.add(fn, arcname=f"sprites/{name}{suf}{ext}")
    print("assets:", os.path.getsize(tar_path) // 1024, "КБ")


def manifest(work, osm_date, planet_name, merge=None):
    """merge — старий manifest.json: регіони з інших id (Ізраїль для України й навпаки) лишаються."""
    meta = json.load(open(os.path.join(work, "regions.json"), encoding="utf-8"))
    def ref(fn):
        p = os.path.join(work, fn)
        return {"file": fn, "size": os.path.getsize(p), "sha256": sha256(p)}
    regs = []
    for rid in (["UA"] if "UA" in meta else []) + sorted(k for k in meta if k != "UA"):
        r = ref(f"map-{rid}.pmtiles")
        r.update({"id": rid, "name": meta[rid]["name"], "bbox": meta[rid]["bbox"]})
        regs.append(r)
    if merge and os.path.isfile(merge):
        try:
            mine = {r["id"] for r in regs}
            old = json.load(open(merge, encoding="utf-8"))["modules"]["map"]["regions"]
            regs += [r for r in old if r["id"] not in mine]
        except Exception as e:
            print("старий маніфест не прочитано:", e)
    now = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    m = {"schema": 1, "generated": now, "osm_date": osm_date, "source": planet_name,
         "license": "ODbL 1.0 — © OpenStreetMap contributors; Protomaps Basemap",
         "modules": {"map": {"tiles_schema": "protomaps-v4", "assets": ref("map-assets.tar"), "regions": regs}}}
    with open(os.path.join(work, "manifest.json"), "w", encoding="utf-8") as g:
        json.dump(m, g, ensure_ascii=False, indent=1)
    tot = sum(r.get("size", 0) for r in regs) / 1e6
    print(f"manifest: {len(regs)} файлів, разом {tot:.0f} МБ")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("step", choices=["regions", "extract", "assets", "manifest"])
    ap.add_argument("--work", default="work")
    ap.add_argument("--adm", help="osmium export → GeoJSON Text Sequence")
    ap.add_argument("--planet", help="URL або файл планетарної збірки Protomaps")
    ap.add_argument("--pmtiles", default="pmtiles")
    ap.add_argument("--maxzoom", type=int, default=15)
    ap.add_argument("--assets-repo", default="basemaps-assets")
    ap.add_argument("--osm-date", default="")
    ap.add_argument("--merge", help="старий manifest.json — регіони з інших id лишаються")
    a = ap.parse_args()
    os.makedirs(a.work, exist_ok=True)
    if a.step == "regions": regions(a.work, a.adm)
    elif a.step == "extract": extract(a.work, a.planet, a.pmtiles, a.maxzoom)
    elif a.step == "assets": assets(a.work, a.assets_repo)
    else: manifest(a.work, a.osm_date, os.path.basename(a.planet or ""), a.merge)
