#P1_Amsterdam_analysis
import os
import geopandas as gpd

script_dir = os.path.dirname(__file__)
block_dir = os.path.join(script_dir,'..','data','amsterdam_wijken_full.json')
arch_dir = os.path.join(script_dir,'..','data','amsterdam_buildings_full.json')

#gpd.read_file
buildings = gpd.read_file(arch_dir)
neighborhoods = gpd.read_file(block_dir)

#allign crs
buildings = buildings.to_crs('EPSG:28992')
neighborhoods = neighborhoods.to_crs('EPSG:28992')

#clean
buildings = buildings[~buildings.geometry.is_empty]
buildings = buildings[buildings.geometry.notna()]
buildings["geometry"] = buildings.geometry.buffer(0)
buildings = buildings[buildings.geometry.is_valid]
buildings = buildings[buildings.geom_type.isin(["Polygon","MultiPolygon"])]

print(buildings.crs)
#save
buildings.to_file(os.path.join(script_dir,'..','data','buildings_clean.gpkg'), driver = "GPKG")

