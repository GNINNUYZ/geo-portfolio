# GeoBIM Portfolio — Yunning Zhang

A portfolio of 7 applied projects in geospatial 3D modelling and point cloud processing, built with real Dutch data (AHN4, BAG, IFC) and Python.

## Projects

| # | Project | Description |
|---|---|---|
| 01 | [Urban Density](01-urban-density/) | Building density analysis of Amsterdam |
| 02 | [Half-edge Engine](02-halfedge-engine/) | Hand-written half-edge data structure |
| 03 | [Terrain Pipeline](03-terrain-pipeline/) | LAZ → TIN → DEM → hydrology |
| 04 | [CityJSON Model](04-cityjson-model/) | Building footprints → LOD 1.2 CityJSON |
| 05 | [IFC → CityJSON](05-ifc2cityjson/) | BIM to CityJSON conversion |
| 06 | [3D Web Platform](06-3d-web-platform/) | FastAPI + PostGIS + CesiumJS viewer |
| 07 | [Point Cloud Toolbox](07-Voxel_filter/) | Voxel filter, KD-tree, RANSAC, ICP |

## Tech Stack

Python, GeoPandas, Rasterio, laspy, PyTorch, PostGIS, CesiumJS

## Quick Start

```bash
pip install -r requirements.txt
# see each project folder for run instructions
```

## Data Sources

- AHN4 laser scanning
- BAG building footprints
- buildingSMART IFC sample
