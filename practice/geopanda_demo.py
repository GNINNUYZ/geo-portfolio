import os
import geopandas as gpd
from pyproj import CRS
from geodatasets import get_path
import matplotlib.pyplot as plt
#找到文件路径
script_dir = os.path.dirname(__file__)
data_dir = os.path.join(script_dir, "..", "data")

#打开文件，创建对象buildings1和blocks1
buildings1 = gpd.read_file(os.path.join(data_dir, "amsterdam_buildings.json"))
blocks1 = gpd.read_file(os.path.join(data_dir, "amsterdam_wijken.json"))
#查看建筑属性
print (buildings1.crs)
print (buildings1.columns)
print (buildings1.shape)
print (buildings1.head())
#用geopanda去掉不可用数据，0数据，只留多边形polygon。
buildings1 = buildings1[buildings1.geometry.is_valid]
buildings1.geometry = buildings1.geometry.buffer(0)
buildings1 = buildings1[buildings1.geometry.geom_type == 'Polygon']
print (buildings1)
#sjoin 建筑polygon进入街区polygon
list1 = gpd.sjoin(buildings1, blocks1, predicate='within')
#创造list1的索引area_m2，blocks1的索引wijk_area_m2/并用*.geometry.area赋值一串面积
list1['area_m2'] = list1.geometry.area
blocks1['wijk_area_m2'] = blocks1.geometry.area
#Z1把所有数据按街区分组做索引，每分区建筑基底面积求和，Z2街区分组做索引，拿出每分区面积
Z1 = list1.groupby('wijknaam')['area_m2'].sum()
Z2 = blocks1.set_index('wijknaam')['wijk_area_m2']
print(Z1/Z2)
result1 = blocks1.copy()
#block1每个索引在Z1里找到对应索引所对应的值除以每个街区的基底面积，结果赋给result1每个街区对应的coverratio
result1['cover_ratio'] = result1['wijknaam'].map(Z1)/ result1['wijk_area_m2']
#输出文件
result1.to_file(os.path.join(data_dir,'coverage_result.geojson'), driver='GeoJSON')
#生成图表，存储文件，显示图表
ax = result1.plot(column='cover_ratio', cmap='YlOrRd', legend=True)
plt.savefig(os.path.join(data_dir, 'coverage_map.png'))
plt.show()