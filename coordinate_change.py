#coordinate_util
#import ifcopenshell.util.placement as plu
from ifcopenshell import geom
import ifcopenshell
import os

scr_path = os.path.dirname(__file__)
data_path = os.path.join(scr_path,'data',"Duplex.ifc")

model = ifcopenshell.open(data_path)
s = geom.settings()
s.set(s.USE_WORLD_COORDS, True)

def get_model(product):
    try:
        sh = geom.create_shape(s, product)
        return  sh.geometry.verts, sh.geometry.faces
    except Exception:
        return None, None


def classify(p):
    t = p.is_a()
    if t in ("IfcWall","IfcWallStandardCase"):
        return "WallSurface"
    if t == "IfcSlab":
        pt = str(p.PredefinedType)
        return {"BASESLAB":"GroundSurface", "ROOF":"RoofSurface"}.get(pt, "FloorSurface")
    return {"IfcRoof": "RoofSurface", "IfcWindow": "Window", "IfcDoor": "Door"}.get(t, "GenericSurface")

vertices, index = [], {}
def add_vertex(x, y, z):
    k = (round(x, 3), round(y, 3), round(z, 3))
    if k not in index:
        index[k] = len(vertices)
        vertices.append([x, y, z])
    return index[k]
    
boundaries, surfaces, values = [], [], []
for p in model.by_type("IfcProduct"):
    verts, faces =get_model(p)
    if verts is None:
        continue
    st = classify(p)
    n = len(verts)//3
    vi = [add_vertex(verts[i*3], verts[i*3+1],verts[i*3+2]) for i in range(n)]
    for j in range(0, len(faces), 3):
        a, b, c = vi[faces[j]], vi[faces[j+1]],vi[faces[j+2]]
        boundaries.append([[a, b, c]])
        surfaces.append({"type": st})
        values.append([len(surfaces)-1])


cityjson = {
    "type":"CityJSON", "version":"1.1",
    "CityObjects":{
        "building-1":{
            "type":"Building",
            "geometry":[{
                "type":"MultiSurface",
                "boundaries":[],
                "semantics":{
                    "surfaces":[],
                    "values": [],
                }
            }],
            "attributes":{}
        }
    },
    "vertices":[]
}


g = cityjson["CityObjects"]["building-1"]["geometry"][0]
g["boundaries"] = boundaries
g["semantics"] = {"surfaces": surfaces, "values":values}
cityjson["vertices"] = vertices

import json
out = os.path.join(scr_path,"05-ifc2cityjson", "outputCity.json")
json.dump(cityjson, open(out, "w"), indent=2)
print("written", out)