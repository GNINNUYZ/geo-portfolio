from utils import Point, Polygon
import numpy as np
import sys
sys.path.insert(0, r'e:\ailearning\geo-portfolio')

#定义geoframe
class geoframe:
    def __init__(self,data,geometry_col="geometry"):
        self.data = data
        self.geometry_col = geometry_col
        
    def __repr__(self):
        return f"GeoDataFrame({len(self.data)} rows)"
    
    def __len__(self):
        return(len(self.data))
    
    def head(self,n):
        return self.data[:n]
    
    def groupby(self,col):
        grouped = {}
        for b in self.data:
            key = b[col]
            if key not in grouped:
                grouped[key] = []
            grouped[key].append(b)
        return grouped


    

b1_geo = Polygon([Point(0,0), Point(20,0), Point(20,15), Point(0,15)])  # 写字楼
b2_geo = Polygon([Point(30,0), Point(40,0), Point(40,10), Point(30,10)]) # 住宅
b3_geo = Polygon([Point(0,30), Point(10,0), Point(0,10), Point(0,30)]) 
b4_geo = Polygon([Point(0,20), Point(20,20), Point(20,35), Point(0,35)])  # 写字楼
b5_geo = Polygon([Point(10,0), Point(20,0), Point(20,10), Point(50,10)]) # 住宅

b1 = {
    "geometry": b1_geo,
    "height" : 50.0,
    "type" : "office"
}
b2 = {
    "geometry": b2_geo,
    "height" : 20.0,
    "type" : "residence"
}
b3 = {
    "geometry": b3_geo,
    "height" : 20.0,
    "type" : "residence"
}
b4 = {
    "geometry": b4_geo,
    "height" : 50.0,
    "type" : "office"
}
b5 = {
    "geometry": b5_geo,
    "height" : 20.0,
    "type" : "residence"
}

gdf = geoframe([b1,b2,b3,b4,b5])
print(gdf)
print(len(gdf))
print(gdf.head(2))
print(gdf.groupby("type"))