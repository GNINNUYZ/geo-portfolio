#polygon
import math

class Point:
     def __init__(self,x,y,z=0):
          self.x = x
          self.y = y
          self.z = z

class polygon:
    def __init__(self,vertices):
        self.vertices = vertices

    def __repr__(self):
         n = len(self.vertices)
         a = self.area()
         return f"Polygon({n}个顶点，面积={a})"
    
    def area(self):
          total = 0
          n = len(self.vertices)
          for i in range(n):
               curr = self.vertices[i]
               nxt = self.vertices[(i+1) % n]
               total += curr.x*nxt.y - curr.y*nxt.x
          return abs(total/2)

p1 = Point(1,2)
p2 = Point(4,5)
p3 = Point(7,8)
p4 = Point(-1,-2)

collectp = [p1,p2,p3,p4]

pol1 = polygon(collectp)
s = pol1.area()
print(s)




