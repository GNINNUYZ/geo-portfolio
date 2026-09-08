# 03 - Terrain Pipeline

Builds a digital terrain model from airborne LiDAR and runs hydrological analysis.

## Pipeline

1. Read AHN4 LAZ point cloud
2. Filter ground points
3. Delaunay TIN / kriging interpolation → DEM
4. Fill depressions, compute D8 flow direction and stream accumulation

## Files

- `delaunay_TIN.py` — TIN / DEM generation
- `kriging.py` — kriging interpolation
- `fillbasin.py` — hydrological preprocessing
- `terrian_calculate.py` — terrain calculation entry
- `pca_normal.py` — normal estimation example
- `pdal_pipeline.json` — PDAL pipeline example
- `*.png` — preview outputs (hillshade, flow, streams)

## Run

```bash
# build DEM
python delaunay_TIN.py
# hydrological analysis
python fillbasin.py
```

## Outputs

DEM preview, hillshade, flow direction, streams.
