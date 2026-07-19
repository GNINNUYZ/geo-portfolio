#footprint
import os
import geopandas as gpd
import numpy as np
import json

scr_path = os.path.dirname(__file__)
GPKG = os.path.join(scr_path, "..", "data", "delft_center_buildings.gpkg")
LAZ = os.path.join(scr_path, "..", "data", "small_dutch.laz")

data0 = gpd.read_file(GPKG)
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
#查coords_dict,根据pointlist里xy查出对应的coords_dict的点序号，再放进buildings[]里 
building = []
for x_list, y_list, z_list in pointlist:
    seq = [coords_dict[(x, y)] for x, y in zip(x_list, y_list)]
    building.append(seq)

print(building[:5])
#定义cityjson
cityjson = {
    "type": "CityJSON","version": "2.0",
    "transform": {"scale": [1,1,1], "translate": [0,0,0]},
    "metadata": {"referenceSystem": "https://www.opengis.net/def/crs/EPSG/28992"},
    "vertices": [[x,y,0] for (x,y) in coords_clean],
    "CityObjects": {}
}
#把得到的buildinglist变成字典
for b, seq in enumerate(building):
    #去掉最后一位
    ring = seq[:-1]
    cityjson["CityObjects"][f"building_{b}"] ={
        "type": "Building",
        "geometry": [{"type": "Solid", "lod":"1.3",
                     "boundaries": [[[ring]]]}]
    }

json.dump(cityjson, open("out.json", "w"))
#生体量，vertice2d:顶点数组，buildingring：建筑id:点序号footprint环，per_building：建筑id：（地面高程，屋顶高程，_）
def riseup(vertices_2d, building_rings, per_building):
    vertices0 = [list(v) for v in vertices_2d]
    solids = {}
#建筑序号，环点序号
    for pid, ring in building_rings.items():
        #对应取出那个建筑的采样数据
        ground, roof, _ = per_building[pid]
        #取出那个建筑的环点序号个数
        n = len(ring)
        #取出建筑的环点序号拷贝
        base = ring[:]
        #取出那个建筑的顶点中的z赋值，对应ground地面
        for vi in base:
            vertices0[vi][2] = ground
        top = []
        for vi in base:
            #取出那个建筑的所有点对应的点坐标
            x, y, _ = vertices0[vi]
            #拿出来的那个点坐标附上Z高度，并加到原vertices0列表中
            vertices0.append([x, y, roof])
            #新加的顶点对应的序号，放进top列表里，此时base列表和top列表中建筑底面点环序号和顶面点环序号一一对应
            top.append(len(vertices0)-1)
        walls = []
        for i in range(n):
            j = (i+1)%n
            #这个建筑的一个墙面，底坐标12，顶坐标21，组成一个墙面，遍历ring生成墙组合
            walls.append((base[i],base[j],top[j], top[i]))
        #放进solid字典里
        solids[pid] = {"base":base, "top":top, "walls":walls}

    for pid, s in solids.items():
        base, top, walls = s["base"], s["top"], s["walls"]
        ground_surf = [base +[base[0]]]
        roof_surf = [top + [top[0]]]
        wall_surfs = [[list(w) + [w[0]]] for w in walls ]

        shell = [ground_surf, roof_surf] + wall_surfs
        boundaries = [shell]
        semantics = ["GroundSurface","RoofSurface"] + ["WallSurface"]*len(walls)
        cityjson["CityObjects"][pid] = {
            "type": "Building",
            "geometry": [{"type":"Solid", "lod":"1.3",
                          "boundaries": boundaries,
                          "semantics": {"surfaces":[{"type":t} for t in semantics]}}]
        }




