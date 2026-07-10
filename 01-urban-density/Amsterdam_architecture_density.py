import os
import geopandas as gpd
import matplotlib.pyplot as plt
import fiona

#建筑,街区数据导入
script_dir = os.path.dirname(__file__)
data_dir = os.path.join(script_dir, "data")
building_dir = os.path.join(data_dir, "buildings_clean.gpkg")
block_dir = os.path.join(data_dir, "amsterdam_wijken_full.json")
#gpd.open
buildings = gpd.read_file(building_dir)
blocks = gpd.read_file(block_dir)
#清洗
buildings["geometry"] = buildings.geometry.buffer(0)
buildings = buildings[buildings.geometry.is_valid]
buildings = buildings[~buildings.geometry.is_empty]
buildings = buildings[buildings.geom_type.isin(["Polygon","MultiPolygon"])]
#对齐数据
buildings = buildings.to_crs('28992')
blocks = blocks.to_crs('28992')
#查看索引
#gpd sjoin predict = within
building_combine = gpd.sjoin(buildings,blocks,predicate="within")
#计算面积
building_combine["area_m2"] = building_combine.geometry.area
blocks["block_area_m2"] = blocks.geometry.area
#groupby
list1 = building_combine.groupby("wijkcode")["area_m2"].sum()
list2 = blocks.set_index("wijkcode")["block_area_m2"]

#计算coverratio
result1 = blocks.copy()
result1 = result1.fillna(0)
result1["cover_ratio"] = result1["wijkcode"].map(list1) / result1["block_area_m2"]
#save csv
result1.to_csv(os.path.join(data_dir, 'coverage_status.csv'), index=False)
#save file
result1.to_file(os.path.join(data_dir, "Amsterdam_architecture_density.geojson"), driver="GeoJSON")
#plt show
fig, ax = plt.subplots(1,3,figsize = (14,12))
schemes = ['equal_interval','quantiles','natural_breaks']
cmaps = ['YlOrRd','YlOrBr',"BuPu"]
for ax, cmap in zip(ax, cmaps):
    result1.plot(column='cover_ratio',scheme = 'quantiles', k = 12,cmap=cmap,legend=True,ax = ax)
    ax.set_title(cmap)
    ax.set_axis_off()

plt.savefig(os.path.join(data_dir, 'Amsterdam_arch_density.png'), dpi=200, bbox_inches='tight')
plt.show()