
from shapely.geometry import Polygon
from shapely.geometry import Point, LineString,MultiPoint,MultiLineString, MultiPolygon

#shapely
a = Point(0.5,0.5)
a1 = Point(100,100)
b = LineString([(0,0),(1,1),(2,3),(5,6)])
b1 = LineString([(0,0),(1,1),(2,3),(5,6),(40,40),(60,60)])
b2 = LineString([(-5,5),(15,5)])
c = Polygon([(0,0), (10,0), (10,10), (0,10)])
print (c.area)
print (b.length)
print (c.bounds)
print (c.centroid)
print (b.coords)
d = MultiPoint([(1,2),(3,4),(5,6)])

cooderlines = ([((0,1),(1,2)),((5,6),(7,8))])
e = MultiLineString(cooderlines)

f = Polygon([(30,30), (50,30), (50,50), (30,50)])
i = Polygon([(300,300), (500,300), (500,500), (300,500)])
g = Polygon([(60,40), (80,40), (80,60), (60,60)])
g1 = Polygon([(60,40), (80,40), (80,60), (60,60)])
g2 = Polygon([(50,50),(55,50),(55,70),(50,70)])
h = MultiPolygon([f, g])

box1 = Polygon([(0,0),(10,0),(10,10),(0,10)])
box11 = Polygon([(0,10),(10,10),(10,20),(0,20)])
box2 = Polygon([(6,5),(12,5),(12,15),(6,15)])
box3 = Polygon([(11,12),(20,12),(20,30),(11,30)])


print (c.contains(a))
print (a.within(c))
print(b.intersects(f))
print (box1.touches(box11))
print (a1.touches(c))
print (f.disjoint(c))
print (i.disjoint(c))
print (box1.overlaps(box2))
print (i.overlaps(c))
print (g.equals(c))
print (g.equals(g1))
print (b2.crosses(c))
print (b1.crosses(c))

buffered1 = b.buffer(1)
print(buffered1)
unioned1 = box1.union(box3)
print(unioned1)
intersection1 = box2.intersection(box1)
print(intersection1)
difference1 = box2.difference(box1)
print(difference1)
sym_difference1 = box3.symmetric_difference(box2)
print(sym_difference1)
