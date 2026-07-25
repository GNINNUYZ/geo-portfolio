#import_cityjson
import json
import os
import asyncio
import asyncpg


scr_path = os.path.dirname(__file__)
data_path = os.path.join(scr_path, "..", 'practice', "out.json")

with open(data_path, encoding="utf-8") as f:
    data = json.load(f)

#pointlist = []

cityobjects = data["CityObjects"]
vertices = data["vertices"]

def get_xyz(idx):
    v = vertices[idx]
    return v[0], v[1], v[2]

async def import_buildings():
    conn = await asyncpg.connect("postgresql://postgres:REDACTED@localhost/geo_portfolio")

    for obj_id, obj in data["CityObjects"].items():
        geom_list = obj.get("geometry", [])
        if not geom_list or geom_list[0].get("type") != "Solid":
            continue

        boundaries = geom_list[0]["boundaries"]

        faces = []
        for shell in boundaries:
            for surface in shell:
                ring = surface[0]
                pts = [get_xyz(vi) for vi in ring]
                pts.append(pts[0])
                faces.append("(({}))".format(
                    ", " .join(f"{x} {y} {z}" for x, y, z in pts)
                ))
        wkt = f"POLYHEDRALSURFACEZ ({', '.join(faces)})"

        attrs = obj.get("attributes", {})
        name = attrs.get("name", obj_id)

        await conn.execute(
            "INSERT INTO buildings (id, name, geom3d, attributes, components) "
            "VALUES ($1, $2, ST_GeomFromText($3, 28992), $4, $5)",
            obj_id, name, wkt, json.dumps(attrs), json.dumps([])
        )

    await conn.close()

asyncio.run(import_buildings())

