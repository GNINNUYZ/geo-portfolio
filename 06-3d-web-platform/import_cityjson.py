#import_cityjson
import json
import os
from dotenv import load_dotenv
load_dotenv()
import asyncio
import asyncpg


scr_path = os.path.dirname(__file__)
data_path = os.path.join(scr_path, "..", '04-cityjson-model', "out.json")

db_url = os.getenv("DATABASE_URL")
if not db_url:
    raise RuntimeError("DATABASE_URL miss, check .env")

db_url = db_url.replace("+asyncpg", "")

with open(data_path, encoding="utf-8") as f:
    data = json.load(f)

#pointlist = []

cityobjects = data["CityObjects"]
vertices = data["vertices"]

def get_xyz(idx):
    v = vertices[idx]
    return v[0], v[1], v[2]

async def import_buildings():
    conn = await asyncpg.connect(db_url)

    for obj_id, obj in data["CityObjects"].items():
        geom_list = obj.get("geometry", [])
        if not geom_list or geom_list[0].get("type") != "Solid":
            continue

        boundaries = geom_list[0]["boundaries"]

        min_z = float('inf')
        footprint_ring = None

        faces = []
        for shell in boundaries:
            for surface in shell:
                ring = surface[0]
                pts = [get_xyz(vi) for vi in ring]
                avg_z = sum(p[2] for p in pts)/ len(pts)
                if avg_z < min_z:
                    min_z = avg_z
                    footprint_ring = [(p[0], p[1]) for p in pts]
                pts.append(pts[0])
                faces.append("(({}))".format(
                    ", " .join(f"{x} {y} {z}" for x, y, z in pts)
                ))
               
        wkt = f"POLYHEDRALSURFACEZ ({', '.join(faces)})"

        attrs = obj.get("attributes", {})
        name = attrs.get("name", obj_id)
        #get point from datasql and make 2dbox(avoid RD AXIS don't fit in CesiumJS show)
        footprint_wkt = "POLYGON(({}))".format(
                        ", ".join(f"{x} {y}" for x, y in footprint_ring)
                        )
        
        await conn.execute(
            "INSERT INTO buildings (id, name, geom3d, footprint, attributes, components) "
            "VALUES ($1, $2, ST_GeomFromText($3, 28992), ST_GeomFromText($4, 28992), $5, $6) "
            "ON CONFLICT (id) DO UPDATE SET "
            "name = EXCLUDED.name, geom3d = EXCLUDED.geom3d, footprint = EXCLUDED.footprint, "
            "attributes = EXCLUDED.attributes, components = EXCLUDED.components",
            obj_id, name, wkt, footprint_wkt, json.dumps(attrs), json.dumps([])
        )

    await conn.close()

asyncio.run(import_buildings())

