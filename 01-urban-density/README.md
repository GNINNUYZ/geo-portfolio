# 01 - Urban Density (Amsterdam)

Analyses building density per neighbourhood in Amsterdam using GeoPandas.

## Pipeline

1. Load building footprints and neighbourhood boundaries
2. Clean geometries and unify CRS (EPSG:28992)
3. Spatial join buildings to neighbourhoods
4. Compute building coverage ratio per neighbourhood

## Files

- `Amsterdam_architecture_density.py` — main script
- `exploratory_analysis.py` — data exploration
- `data/coverage_map.png`, `data/building_distribution.png` — result maps

## Run

```bash
python Amsterdam_architecture_density.py
```

## Output

- `data/coverage_status.csv`
- `data/Amsterdam_architecture_density.geojson`
- PNG result maps
