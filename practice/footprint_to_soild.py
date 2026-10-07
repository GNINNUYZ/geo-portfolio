#footprint_to_soild
from shapely.geometry import shape
import geopandas as gpd
import os

scr_path = os.path.dirname(__file__)
data_path = os.path.join(scr_path, '..', '01-urban-density','data', 'buildings_clean.gpkg')

data0 = gpd.read_file(data_path)
print(type(data0))
print(data0.columns)

Pointpool = []

