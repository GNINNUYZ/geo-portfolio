#main
import os
import json
from fastapi import FastAPI, Depends, Query, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy import text
from pydantic import BaseModel

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+asyncpg://postgres:REDACTED@localhost:5432/geo_portfolio"
)

engine = create_async_engine(DATABASE_URL, echo=False)

AsyncSessionLocal = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

# AsyncSession = Depends(get_db)
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session

app = FastAPI(title="GeoBIM API", version="1.0")

class SpatialQuery(BaseModel):
    geometry: dict
    relation: str = "intersects"

#sql all buildings
@app.get("/api/buildings")
async def get_buildings(
    bbox: str = Query(None, description="xmin,ymin,xmax,ymax"),
    db: AsyncSession = Depends(get_db)
):
    if bbox:
        coords = [float(x) for x in bbox.split(",")]
        sql = text("""
            SELECT id, name, attributes,
                ST_AsGeoJSON(ST_Force2D(geom3d)) AS footprint
            FROM buildings
            WHERE geom3d && ST_MakeEnvelope(:xmin, :ymin, :xmax, :ymax, 28992)
            LIMIT 100
        """)
        result = await db.execute(sql, {
            "xmin": coords[0], "ymin": coords[1],
            "xmax": coords[2], "ymax": coords[3]
        })

    else:
        result = await db.execute(
            text("SELECT id, name, attributes FROM buildings LIMIT 100")
        )

        rows = result.fetchall()
        return [{"id": row[0], "name": row[1], "attributes": row[2]} for row in rows]

    rows = result.fetchall()
    features = []
    for row in rows:
        features.append({
            "type": "Feature",
            "geometry": json.loads(row[3]),
            "properties": {
                "id": row[0],
                "name": row[1],
                "attributes": row[2]
            }
        })
    return {"type": "FeatureCollection", "features": features}
@app.get("/api/buildings/{building_id}")
async def get_building(building_id: str, db: AsyncSession = Depends(get_db)):
    """
    返回单个建筑的完整信息，包括 WKT 格式的 3D 几何。
    示例: /api/buildings/b0
    """
    sql = text("""
        SELECT id, name, attributes, components, ST_AsText(geom3d) AS wkt
        FROM buildings
        WHERE id = :id
    """)
    result = await db.execute(sql, {"id": building_id})
    row = result.fetchone()
    if not row:
        raise HTTPException(status_code=404, detail=f"Building '{building_id}' not found")
    return {
        "id": row[0],
        "name": row[1],
        "attributes": row[2],    # JSONB 自动转成 Python dict
        "components": row[3],    # JSONB 自动转成 Python list
        "geometry_wkt": row[4]   # WKT 字符串，例如 "POLYHEDRALSURFACEZ (...)"
    }


# --- 端点 3: 查询建筑的构件列表 ---

@app.get("/api/buildings/{building_id}/components")
async def get_components(building_id: str, db: AsyncSession = Depends(get_db)):
    """
    只返回建筑的构件列表。前端点击建筑后调这个接口展示构件。
    示例: /api/buildings/b0/components
    """
    result = await db.execute(
        text("SELECT components FROM buildings WHERE id = :id"),
        {"id": building_id}
    )
    row = result.fetchone()
    if not row:
        raise HTTPException(status_code=404, detail=f"Building '{building_id}' not found")
    return row[0]  # JSONB 列，直接返回

@app.get("/api/scene/buildings")
async def get_hight( db : AsyncSession = Depends(get_db)):
    result = await db.execute(
        text("SELECT id, name, attributes, "
        "ST_AsGeoJSON(ST_Transform(ST_Envelope(geom3d), 4326)) AS footprint, "
        "ST_ZMax(geom3d) - ST_ZMin(geom3d) AS height, "
        "ST_ZMin(geom3d) AS ground_z " 
        "FROM buildings")
    )
    rows = result.fetchall()
    features = []
    for row in rows:
        features.append({
            "type":"Feature",
            "geometry": json.loads(row[3]),
            "properties":{
                "id": row[0],
                "name": row[1],
                "height": float(row[4]),
                "ground_z": float(row[5]),
                "attributes": row[2]
            }
        })
    return {"type": "FeatureCollection","features":features}

# --- 端点 4: 3D 空间查询 ---

@app.post("/api/query/spatial")
async def spatial_query(query: SpatialQuery, db: AsyncSession = Depends(get_db)):
    """
    接收一个 GeoJSON 几何体，返回与之 3D 相交的建筑。
    Body 示例:
    {
      "geometry": {"type": "Point", "coordinates": [84995, 443860, 3.0]},
      "relation": "intersects"
    }
    """
    # 把 GeoJSON dict 转成 WKT 字符串
    from shapely.geometry import shape
    geom = shape(query.geometry)
    wkt = geom.wkt

    sql = text("""
        SELECT id, name, attributes
        FROM buildings
        WHERE ST_3DIntersects(geom3d, ST_GeomFromText(:wkt, 28992))
    """)
    result = await db.execute(sql, {"wkt": wkt})
    rows = result.fetchall()
    return {
        "buildings": [
            {"id": row[0], "name": row[1], "attributes": row[2]}
            for row in rows
        ]
    }

FRONTEND_DIR = os.path.join(os.path.dirname(__file__), "frontend")
TILES_DIR = os.path.join(os.path.dirname(__file__), "tiles")

@app.get("/")
async def root():
    return FileResponse(os.path.join(FRONTEND_DIR, "index.html"))

if os.path.isdir(TILES_DIR):
    app.mount("/tiles", StaticFiles(directory=TILES_DIR, name = "tiles"))

if os.path.isdir(FRONTEND_DIR):
    app.mount("/static", StaticFiles(directory=FRONTEND_DIR), name="static")

