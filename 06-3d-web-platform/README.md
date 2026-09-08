# 06 - 3D Web Platform

A web platform for viewing and querying CityJSON buildings in a browser.

## Pipeline

1. Import CityJSON into PostGIS as 3D geometries (EPSG:28992)
2. Expose REST endpoints with FastAPI (SQLAlchemy async)
3. Visualize in CesiumJS frontend

## Files

- `import_cityjson.py` — PostGIS import
- `main.py` — FastAPI backend
- `sql.sql` — database schema
- `frontend/index.html` — CesiumJS viewer
- `backend/requirements.txt`

## Setup

1. Create a PostGIS database and run `sql.sql`
2. Set `DATABASE_URL` in `.env`
3. Import CityJSON:

```bash
python import_cityjson.py
```

## Run

```bash
python main.py
```

Open `http://localhost:8000`

## API

- `GET /api/buildings` — list buildings / bbox query
- `GET /api/scene/buildings` — building heights for the scene
- `POST /api/query/spatial` — 3D spatial query
