#pyproj
import numpy as np
import os
os.environ["PROJ_NETWORK"] = "OFF"
from pyproj import Transformer
from pyproj import CRS

crs1 = CRS.from_epsg(4326)
crs2 = CRS.from_epsg(28992)
transformer = Transformer.from_crs(crs1, crs2)
transformer1 = transformer.transform(52.3676,4.9041)
print (transformer1)

lats = np.array([52.3676, 52.3700, 52.3600, 52.3750, 52.3650])
lons = np.array([4.9041, 4.9100,  4.8800,  4.8950,  4.9200])

xx, yy = transformer.transform(lats,lons)
print(xx,yy)