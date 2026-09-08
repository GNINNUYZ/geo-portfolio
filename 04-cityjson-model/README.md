# 04 - CityJSON Model

Reconstructs simple LOD 1.2 3D city models from building footprints and airborne point clouds.

## Pipeline

1. Load Delft building footprints (GeoJSON)
2. Crop AHN4 points inside each building footprint
3. Estimate ground and roof heights from points
4. Build CityJSON solids with semantic surfaces

## Files

- `footprint.py` — main script
- `delft_50.geojson` — building footprints
- `out.json` — output CityJSON

## Run

```bash
python footprint.py
```

## Output

`out.json` — CityJSON LOD 1.2 model
