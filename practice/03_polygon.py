#Point类
class Point:
    def __init__(self,x,y):
        self.x = x
        self.y = y
#Circle类
class Circle:
    def __init__(self,center,radius):
        self.center = center
        self.radius = radius

circle1 = Circle(Point(5,6),10)
circle1.center = Point(150,100)
circle1.radius = 75
#Target类
class Target:
    def __init__(self,x,y):
        self.x = x
        self.y = y

target1 = Target(150,105)
#功能，判断target实例和circle实例关系
def target_detect(target,circle):
    x_distance = target.x - circle.center.x
    y_distance = target.y - circle.center.y
    p_distance = (x_distance**2 + y_distance**2)**0.5
    if circle.radius >= p_distance:
        print(f'点在圆内')
    else:
        print(f'点在圆外')

target_detect(target1,circle1)
#正方形
class Rectangle:
    def __init__(self,corner,x_length,y_length):
        self.corner = corner
        self.p1x = corner.x
        self.p1y = corner.y
        self.p2x = corner.x
        self.p2y = corner.y + y_length
        self.p3x = corner.x + x_length
        self.p3y = corner.y
        self.p4x = corner.x + x_length
        self.p4y = corner.y + y_length
        

rectangle1 = Rectangle(Point(150,80),20,10)
#正方形和圆形关系
def rect_in_circle(rectangle,circle):
    p1_d = ((rectangle.p1x - circle.center.x)**2 + (rectangle.p1y - circle.center.y)**2)**0.5
    p2_d = ((rectangle.p2x - circle.center.x)**2 + (rectangle.p2y - circle.center.y)**2)**0.5
    p3_d = ((rectangle.p3x - circle.center.x)**2 + (rectangle.p3y - circle.center.y)**2)**0.5
    p4_d = ((rectangle.p4x - circle.center.x)**2 + (rectangle.p4y - circle.center.y)**2)**0.5
    if p1_d <= circle.radius and p2_d <= circle.radius and p3_d <= circle.radius and p4_d <= circle.radius:
        print('矩形在圆内')
    else:
        print('矩形在圆外')

rect_in_circle(rectangle1,circle1)