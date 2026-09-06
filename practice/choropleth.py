#footprint
import os
import geopandas as gpd
import numpy as np
import json

scr_path = os.path.dirname(__file__)
data_path = os.path.join(scr_path, 'data', 'delft_buildings.gpkg')

data0 = gpd.read_file(data_path)
data0 = data0.to_crs(28992)

print(data0.iterrows)

pointlist = []
x_all = []
y_all = []
z_all = []

for idx, row in data0.iterrows():
    geom = row.geometry

    if geom != None:
        coords = list(geom.exterior.coords)
        if len(coords[0]) == 3:
            x_coords = [c[0] for c in coords]
            y_coords = [c[1] for c in coords]
            z_coords = [c[2] for c in coords]
        else:
            x_coords = [c[0] for c in coords]
            y_coords = [c[1] for c in coords]
            z_coords = []

        pointlist.append((x_coords, y_coords,z_coords))

coords_clean = []
for x_list, y_list, z_list in pointlist:
    for x, y in zip(x_list, y_list):
        if(x, y) not in coords_clean:
            coords_clean.append((x, y))
print(len(coords_clean))

coords_dict = {i:v for v, i in enumerate(coords_clean)}
print(type(coords_dict))

building = []
for x_list, y_list, z_list in pointlist:
    seq = [coords_dict[(x, y)] for x, y in zip(x_list, y_list)]
    building.append(seq)

print(building[:5])

cityjson = {
    "type": "CityJSON","Version": "1.0",
    "transform": {"scale": [1,1,1], "translate": [0,0,0]},
    "metadata": {"referenceSystem": "https://opengis.net/def/crs/EPSG/28992"},
    "vertices": [[x,y,0] for (x,y) in coords_clean],
    "CityObjects": {}
}
for b, seq in enumerate(building):
    ring = seq[:-1]
    cityjson["CityObjects"][f"building_{b}"] ={
        "type": "Building",
        "geometry": [{"type": "Solid", "lod":"1.3",
                     "boundaries": [[[ring]]]}]
    }

json.dump(cityjson, open("out.json", "w"))