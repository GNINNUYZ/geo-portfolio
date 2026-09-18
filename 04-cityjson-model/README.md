# 04 - CityJSON Model

Reconstructs simple block (LoD1) 3D city models from building footprints and airborne point clouds — 50 buildings in Delft.

## Pipeline

1. Load Delft building footprints (GeoJSON)
2. Crop AHN4 points around and inside each building footprint
3. Estimate ground and roof heights from points
4. Build CityJSON solids with semantic surfaces

## Height estimation (definitions)

Airborne LiDAR has **no ground returns inside a building footprint** — the roof blocks the pulse. Measured on `delft_50_crop.laz`: all 14,817 points inside the first footprint belong to class 6 (building). Ground elevation therefore cannot come from inside the footprint.

| value | source |
|---|---|
| `ground` | **median** of class 2 (ground) returns within a **6 m buffer** around the footprint |
| `roof` | **90th percentile** of class 6 (building) returns **inside** the footprint |
| `height` | `roof - ground` |

## Results

Input `delft_50_crop.laz` (AHN4): 5,406,139 points; classes present: 1 (unclassified), 2 (ground), 6 (building), 9 (water), 14, 26.

- Buildings reconstructed: **50**
- Ground elevation: **−1.38 … 0.19 m** (Delft is around NAP ≈ 0)
- Building height: **2.26 … 9.75 m**, mean **7.20 m**
- Vertices in `out.json`: 605

## Files

- `footprint.py` — main script
- `delft_50.geojson` — building footprints
- `out.json` — output CityJSON

## Run

```bash
python footprint.py
```

## Output

`out.json` — CityJSON 1.1 model: one `Solid` per building, with semantic surfaces `GroundSurface` / `RoofSurface` / `WallSurface`.

## Known issues

- **LoD level = 1.2** (settled 2026-09-16): each building gets one uniform height, which is LoD1.2. Per the [3DBAG schema docs](https://docs.3dbag.nl/en/schema/concepts/) (following Biljecki, Ledoux & Stoter 2016): *"the distinction between LoD1.2 and LoD1.3 is that LoD1.3 distinguishes between significant height differences within one building, while in case of LoD1.2 the whole model has a uniform height."* The script now writes `"lod": "1.2"` (it previously wrote `1.3`). ⚠️ `out.json` needs one re-run to pick this up.
- **No coordinate quantisation**: `transform.scale = [1,1,1]` while vertices are floating point. CityJSON 1.1 expects quantised integer vertices, so the file does not pass `cjio validate`.
- **Ground sampling area**: ground is taken from a circular 6 m buffer (not a ring excluding the footprint). Since no ground returns exist inside the footprint, the difference is immaterial — but a proper solution is to sample the terrain DEM from `03-terrain-pipeline`.
