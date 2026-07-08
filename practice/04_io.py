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
#输入数据，判断是否为Point类，转化为WKT格式    
def to_wkt(geom):
    if isinstance(geom,Point):
        return f"POINT ({geom.x} {geom.y} {geom.z})"
    
#从WKT取数据，转化为Point格式
def from_wkt(p):
    sel_p = p[7:-1]
    x , y, z = sel_p.split(' ')
    x1 , y1, z1 = float(x),float(y),float(z)
    return Point(x1,y1,z1)

#with open，读文件，转为point list
def readFile(path):
    file1 =[]
    with open(path,'r') as f:
        for line in f:
            s = from_wkt(line.strip())
            file1.append(s)
    return file1
#with open ，创建文件，写成WKT格式
def createFile(geoms,name):
    with open(name,'w') as f:
        for g in geoms:
            f.write(to_wkt(g) + '\n')
    
p1 = Point(1,2,3)
p2 = Point(4,5,6)

createFile([p1,p2], 'test.wkt')
result = readFile('test.wkt')
print(result)
print(p2.calc_d(p1))
