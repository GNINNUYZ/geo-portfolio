import shapely
from shapely.geometry import Polygon

Z = Polygon([[0, 0], [1, 0], [1, 1], [0, 1], [0, 0]]).minimum_clearance
print(Z)

from shapely.geometry import Point
Z = Point(1,2).distance(Point(5,6))
print(Z)