#exploratory_analysis
import os
import geopandas as gpd
import matplotlib.pyplot as plt

script_dir = os.path.dirname(__file__)
bag1_dir = os.path.join(script_dir,'..','data','amsterdam_buildings.json')
cbs1_dir = os.path.join(script_dir,'..','data','amsterdam_wijken.json')

#gpd打开
arch1 = gpd.read_file(bag1_dir)
block1 = gpd.read_file(cbs1_dir)

#清洗数据
arch1.geometry = arch1.geometry.buffer(0)
arch1 = arch1[arch1.geometry.is_valid]
arch1 = arch1[arch1.geometry.geom_type.isin(['Polygon', 'MultiPolygon'])]

#建筑，街区 sjoin
list1 = gpd.sjoin(arch1, block1, predicate='within')
print(type(list1))
#街区提取geometry，通过geopanda计算area
block1['wijk_area_m2'] = block1.geometry.area
#建筑geopanda计算area
list1['area_m2'] = list1.geometry.area

#按街区groupby，输出每栋街区建筑数量
Z1 = list1.groupby('wijknaam')['area_m2'].sum()
Z2 = block1.set_index('wijknaam')['wijk_area_m2']
print(Z1/Z2)

#街区面积分布直方图
plt.figure()
plt.hist(Z2, bins=50)
plt.show()
#建筑面积分布直方图
plt.figure()
plt.hist(Z1, bins=50)
plt.show()
#街区建筑数量分布
counts = list1.groupby('wijknaam').size()
plt.figure()
plt.hist(counts, bins=50)
plt.show()
#街区建筑密度
result1 = block1.copy()
result1['cover_ratio'] = result1['wijknaam'].map(Z1)/result1['wijk_area_m2']
plt.figure()
ax = result1.plot(column='cover_ratio', cmap='YlOrRd', legend=True)
plt.show()
