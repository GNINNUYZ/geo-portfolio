"""
Download AHN4 DTM for Amsterdam Centrum via PDOK WCS 1.0.0.
"""
from owslib.wcs import WebCoverageService
from pathlib import Path

WCS_URL = "https://service.pdok.nl/rws/ahn/wcs/v1_0"

# Amsterdam Centrum area (EPSG:28992 RD New)
XMIN, YMIN = 121_800, 486_900
XMAX, YMAX = 122_200, 487_300  # 400m x 400m

WIDTH = 800    # 0.5m resolution
HEIGHT = 800

OUTPUT = Path(__file__).parent / "data" / "ahn4_dtm_amsterdam.tif"

print("Connecting to PDOK AHN4 WCS 1.0.0...")
wcs = WebCoverageService(WCS_URL, version="1.0.0")

dtm_id = "dtm_05m"
bbox = (XMIN, YMIN, XMAX, YMAX)
bbox_str = f"({XMIN},{YMIN},{XMAX},{YMAX})"

print(f"Coverage: {dtm_id}")
print(f"BBOX:     {bbox_str} ({XMAX-XMIN}m x {YMAX-YMIN}m)")
print(f"Size:     {WIDTH}x{HEIGHT} px")

# WCS 1.0.0 GetCoverage with explicit bbox parameter
bbox_tuple = (XMIN, YMIN, XMAX, YMAX)

response = wcs.getCoverage(
    identifier=dtm_id,
    bbox=bbox_tuple,
    crs="EPSG:28992",
    format="GeoTIFF",
    width=WIDTH,
    height=HEIGHT,
    resx=(XMAX - XMIN) / WIDTH,
    resy=(YMAX - YMIN) / HEIGHT,
    timeout=120,
)

OUTPUT.parent.mkdir(parents=True, exist_ok=True)
OUTPUT.write_bytes(response.read())
size_mb = OUTPUT.stat().st_size / (1024 * 1024)
print(f"Done: {OUTPUT} ({size_mb:.1f} MB)")
