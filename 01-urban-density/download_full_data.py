"""
Download full Amsterdam data for P1 (urban building density).

Sources (PDOK, official Dutch open geodata, all EPSG:28992 RD New):
  - CBS Wijk- en Buurtkaart 2024  -> wijken (neighbourhoods), WFS + CQL filter
  - BAG pand (building footprints) -> OGC API Features, paged over Amsterdam bbox

Amsterdam buildings are filtered by BAG identificatie prefix "0363"
(= Amsterdam gemeentecode), which drops neighbouring municipalities that the
bounding box otherwise pulls in.

Outputs (data/):
  - amsterdam_wijken_full.json
  - amsterdam_buildings_full.json
"""
import json
import time
from pathlib import Path

import requests

DATA = Path(__file__).resolve().parent.parent / "data"
CRS_28992 = "http://www.opengis.net/def/crs/EPSG/0/28992"
AMSTERDAM_GEMEENTECODE = "0363"  # BAG identificatie prefix

WIJKEN_WFS = "https://service.pdok.nl/cbs/wijkenbuurten/2024/wfs/v1_0"
BAG_ITEMS = "https://api.pdok.nl/kadaster/bag/ogc/v2/collections/pand/items"

CRS_HEADER = {
    "type": "name",
    "properties": {"name": "urn:ogc:def:crs:EPSG::28992"},
}


def _get(url, params=None, tries=5, timeout=180):
    """GET with retry/backoff."""
    for attempt in range(tries):
        try:
            r = requests.get(url, params=params, timeout=timeout)
            r.raise_for_status()
            return r
        except Exception as e:
            wait = 2 * (attempt + 1)
            print(f"  ! retry {attempt + 1}/{tries} in {wait}s: {e}")
            time.sleep(wait)
    raise RuntimeError(f"GET failed after {tries} tries: {url}")


def download_wijken():
    print("[1/2] CBS wijken (Amsterdam) via WFS ...")
    params = {
        "service": "WFS",
        "version": "2.0.0",
        "request": "GetFeature",
        "typeNames": "wijkenbuurten:wijken",
        "outputFormat": "application/json",
        "srsName": "EPSG:28992",
        "CQL_FILTER": "gemeentenaam='Amsterdam'",
    }
    d = _get(WIJKEN_WFS, params).json()
    feats = d["features"]
    out = DATA / "amsterdam_wijken_full.json"
    out.write_text(json.dumps(d))
    print(f"      wijken: {len(feats)}  ->  {out.name}")

    # bounding box of all wijken (RD New)
    xs, ys = [], []
    for f in feats:
        minx, miny, maxx, maxy = _feature_bounds(f["geometry"])
        xs += [minx, maxx]
        ys += [miny, maxy]
    bbox = (min(xs), min(ys), max(xs), max(ys))
    print(f"      bbox (28992): {tuple(round(v) for v in bbox)}")
    return bbox


def _feature_bounds(geom):
    def coords(g):
        if isinstance(g[0], (int, float)):
            yield g
        else:
            for sub in g:
                yield from coords(sub)

    pts = list(coords(geom["coordinates"]))
    xs = [p[0] for p in pts]
    ys = [p[1] for p in pts]
    return min(xs), min(ys), max(xs), max(ys)


def download_buildings(bbox):
    print("[2/2] BAG pand (building footprints) via OGC API Features ...")
    params = {
        "f": "json",
        "limit": 1000,
        "bbox": ",".join(str(v) for v in bbox),
        "bbox-crs": CRS_28992,
        "crs": CRS_28992,
    }
    feats = []
    url, use_params, page = BAG_ITEMS, params, 0
    while url:
        d = _get(url, use_params).json()
        got = d.get("numberReturned", len(d["features"]))
        feats.extend(d["features"])
        page += 1
        if page % 10 == 0 or got < 1000:
            print(f"      page {page}: +{got}  total {len(feats)}")
        nxt = [l["href"] for l in d.get("links", []) if l.get("rel") == "next"]
        if nxt and got > 0:
            url, use_params = nxt[0], None  # next link already carries params
        else:
            url = None

    # keep Amsterdam only (identificatie starts with gemeentecode 0363)
    ams = [
        f
        for f in feats
        if str(f["properties"].get("identificatie", "")).startswith(AMSTERDAM_GEMEENTECODE)
    ]
    print(f"      fetched (bbox): {len(feats)}   Amsterdam (0363): {len(ams)}")

    fc = {
        "type": "FeatureCollection",
        "name": "pand",
        "crs": CRS_HEADER,
        "features": ams,
    }
    out = DATA / "amsterdam_buildings_full.json"
    out.write_text(json.dumps(fc))
    print(f"      -> {out.name}")


if __name__ == "__main__":
    DATA.mkdir(parents=True, exist_ok=True)
    bbox = download_wijken()
    download_buildings(bbox)
    print("Done.")
