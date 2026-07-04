import math
class Point:
    def __init__(self,x,y,z=0):
        self.x = x
        self.y = y
        self.z = z
    def __repr__(self):
        return f"Point({self.x}, {self.y}, {self.z})"
    def calc_d(self,other):
        d = math.sqrt((self.x-other.x)**2 + (self.y-other.y)**2+ (self.z-other.z)**2)
        return d

class Polygon:
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
    
def to_wkt(geom):
    if isinstance(geom,Point):
        return f"POINT ({geom.x} {geom.y} {geom.z})"
    

def from_wkt(p):
    sel_p = p[7:-1]
    x , y, z = sel_p.split(' ')
    x1 , y1, z1 = float(x),float(y),float(z)
    return Point(x1,y1,z1)


def readFile(path):
    file1 =[]
    with open(path,'r') as f:
        for line in f:
            s = from_wkt(line.strip())
            file1.append(s)
    return file1

def createFile(geoms,name):
    with open(name,'w') as f:
        for g in geoms:
            f.write(to_wkt(g) + '\n')
    