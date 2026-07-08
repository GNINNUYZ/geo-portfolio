# W3D6: GDAL/OGR 底层 API 概览
# 用 Fiona 学 OGR 概念 —— Fiona = OGR 的 Pythonic 封装
#
# GDAL/OGR 概念映射：
#   ogr.Open(path)          → fiona.open(path)
#   ds.GetLayer(0)          → collection (直接就是 layer)
#   layer.GetFeatureCount() → len(collection)
#   layer.GetNextFeature()  → for feature in collection
#   feature.GetGeometryRef()→ feature['geometry']
#   feature.GetField("x")   → feature['properties']['x']
#   feature.GetFID()        → feature['id']
#   layer.GetSpatialRef()   → collection.crs
#   layer.GetGeomType()     → collection.schema['geometry']

import fiona
import os

script_dir = os.path.dirname(__file__)
data_dir = os.path.join(script_dir, '..', 'data')

# 1. 打开数据源 = ogr.Open()
#    列出所有可用的 OGR Driver
print("=== OGR Drivers (内置) ===")
for name in sorted(fiona.supported_drivers.keys()):
    print(f"  {name}: {'r/w' if 'w' in fiona.supported_drivers[name] else 'read-only'}")

print()

# 2. 读 GeoJSON = ogr.Open + GetLayer
#    Fiona 一步到位: open 返回的就是 layer (collection)
geojson_path = os.path.join(data_dir, 'amsterdam_wijken.json')
print(f"=== 打开数据源: {geojson_path} ===")

with fiona.open(geojson_path) as src:
    # 3. 元数据 —— 等价于 layer 的各种 Get 方法
    print(f"Driver:   {src.driver}")           # GetDriver().GetName()
    print(f"CRS:      {src.crs}")              # GetSpatialRef()
    print(f"几何类型: {src.schema['geometry']}") # GetGeomType()
    print(f"字段数:   {len(src.schema['properties'])}")
    print(f"要素数:   {len(src)}")              # GetFeatureCount()
    print(f"范围:     {src.bounds}")            # GetExtent()

    print()

    # 4. 字段定义 —— 等价于 GetFieldDefn 遍历
    print("=== 字段定义 (Schema) ===")
    for field_name, field_type in src.schema['properties'].items():
        print(f"  {field_name}: {field_type}")

    print()

    # 5. 遍历 Feature —— 等价于 GetNextFeature 循环
    print("=== 前 5 个 Feature 遍历 ===")
    for i, feature in enumerate(src):
        if i >= 5:
            break
        fid = feature['id']                    # GetFID()
        props = feature['properties']          # GetField()
        geom_type = feature['geometry']['type'] # GetGeometryRef().GetGeometryName()

        print(f"  FID={fid}")
        print(f"    几何类型: {geom_type}")
        print(f"    属性: {dict(list(props.items())[:3])}")  # 只显示前3个字段
        print()

# 6. 对比 GeoPandas —— 同一组操作的高层 vs 底层
print("=== 对比: GeoPandas (高层) vs Fiona (底层) ===")
import geopandas as gpd

# GeoPandas 一行读
gdf = gpd.read_file(geojson_path)
print(f"GeoPandas: {len(gdf)} 行, {len(gdf.columns)} 列")

# Fiona 逐行读（可以控制内存、做流式处理）
count = 0
with fiona.open(geojson_path) as src:
    for feature in src:
        count += 1
print(f"Fiona:     {count} 个 feature")

# 7. 写 GeoJSON —— 等价于 CreateDataSource + CreateLayer + CreateFeature
output_path = os.path.join(script_dir, 'ogr_demo_output.geojson')
schema = {
    'geometry': 'Point',
    'properties': {'name': 'str', 'value': 'float'}
}

with fiona.open(output_path, 'w', driver='GeoJSON', crs='EPSG:4326', schema=schema) as dst:
    # 建 feature
    feature = {
        'geometry': {'type': 'Point', 'coordinates': [4.895, 52.370]},  # Amsterdam center
        'properties': {'name': 'test_point', 'value': 42.0}
    }
    dst.write(feature)  # 等价于 CreateFeature
    print(f"\n写了一个 feature 到: {output_path}")

# 8. OGR 风格的低级属性访问
print("\n=== 元数据详细 ===")
with fiona.open(geojson_path) as src:
    # 等价于 layer 的各种标志
    meta = src.meta
    print(f"meta keys: {list(meta.keys())}")
    print(f"  driver:   {meta['driver']}")
    print(f"  schema:   {meta['schema']}")
    print(f"  crs:      {meta['crs']}")
    # encoding: layer.GetEncoding()
    # 但 Fiona 已自动处理 UTF-8
