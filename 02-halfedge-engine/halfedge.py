#eular pointcare
import os

script_dir = os.path.dirname(__file__)
data_dir = os.path.join(script_dir,'..','data','cube.obj')

class Vertex:
    def __init__(self,x,y,z,halfedge=None):
        self.x = x
        self.y = y
        self.z = z
        self.halfedge = halfedge
    def __repr__(self):
        return f"Vertex({self.x},{self.y},{self.z},{self.halfedge})"

class Face:
    def __init__(self,halfedge = None):
        self.halfedge= halfedge

    def __repr__(self):
        return f"Face({self.halfedge})"
    
class HalfEdge:
    def __init__(self):
        self.origin = None
        self.twin = None
        self.next = None
        self.prev = None
        self.face = None

class Mesh:
    def __init__(self):
        self.vertices = []
        self.faces = []
        self.halfedges = []

    def face_vertices(self,face):
        he = face.halfedge
        vertices = []
        while True:
            vertices.append(he.origin)
            he = he.next
            if he == face.halfedge:
                break
        return vertices

    def vertices_faces(self,v):
        he = v.halfedge
        faces = []
        cur = he
        while True:
            faces.append(cur.face)
            if cur.twin is None:
                break
            cur = cur.twin.next
            if cur == he:
                return faces
        cur = he
        while True:
            cur = cur.prev
            if cur.twin == None:
                break
            cur = cur.twin
            faces.insert(0,cur.face)
        return faces

    def adjacent_faces(self,face):
        he = face.halfedge
        faces = []
        while True:
            if he.twin != None:
                faces.append(he.twin.face)
            he = he.next
            if he == face.halfedge:
                break
        return faces

    def boundary_edges(self):
        boundarys = []
        for face in self.faces:
            he = face.halfedge
            while True:
                if he.twin == None:
                    boundarys.append(he)
                he = he.next
                if he == face.halfedge:
                    break
        return boundarys

    def build_from_obj(self,path):
        edge_map1 = dict()
        with open (path,'r') as f:
            for line in f:
                parts = line.strip().split()               
                if not parts:
                    continue
                if parts[0] == 'v':
                    x, y, z = float(parts[1]), float(parts[2]), float(parts[3])
                    self.vertices.append(Vertex(x, y, z))
                elif parts[0] == 'f':
                    face = Face()
                    list1 = parts[1:]
                    list1_index = [int(p) - 1 for p in list1]
                    for j in range(len(list1_index)):
                        startpoint = self.vertices[list1_index[j]]
                        endpoint = self.vertices[list1_index[(j+1)% len(list1_index) ]]
                        he = HalfEdge()
                        he.origin = startpoint
                        he.face = face
                        self.halfedges.append(he)
                        edge_map1[(id(startpoint),id(endpoint))] = he
                    self.faces.append(face)
                    n = len(list1_index)
                    face_hes = self.halfedges[-n:]
                    for m in range(n):
                        face_hes[m].next = face_hes[(m+1)%n]
                        face_hes[m].prev = face_hes[(m-1)%n]
                    face.halfedge = face_hes[0]
        #twin
        for he in self.halfedges:
            v_origin = he.origin
            v_next_origin = he.next.origin
            key = (id(v_next_origin),id(v_origin))
            if key in edge_map1:
                twin = edge_map1[key]
                he.twin = twin
                twin.twin = he
        for he in self.halfedges:
            if he.origin.halfedge == None:
                he.origin.halfedge = he

    def is_valid(self):
        v1 = len(self.vertices)
        e1 = len(self.halfedges)//2
        f1 = len(self.faces)
        return v1 - e1 + f1 == 2

    def count_vertices_edge(self,v):
        v0 = v
        count = 0
        for he in self.halfedges:  
            if he.origin == v0:
                count += 1
        return count

    def walk_vertices(self,v):
        start = v.halfedge
        if start is None:
            return 0
        he = start
        count = 0
        while True:
            count += 1
            if he.twin is None:
                break
            he = he.twin.next
            if he is start:
                break 
        return count
    
    def is_2_manifold(self):
        result = []
        for vx in self.vertices:
            a = self.count_vertices_edge(vx)
            b = self.walk_vertices(vx)
            if a == b or a == b+1:
                result.append(True)
            else:
                result.append(False)
        return result
        
    def to_obj(self):
        path = os.path.join(script_dir,'..','data','cube_t0_obj_test.obj')
        with open(path,'w') as f:
            for v in self.vertices:
                f.write(f'v {v.x} {v.y} {v.z}\n')

            index = {v:i for i,v in enumerate(self.vertices,start=1)}
            for face in self.faces:
                verts = self.face_vertices(face)
                f.write('f' +' ')
                for v in verts:
                    f.write(f' {str(index[v])}')
                f.write('\n')
 
#test
m = Mesh()
m.build_from_obj(data_dir)
print(len(m.vertices))
print(len(m.faces))
print(len(m.halfedges))
print(len(m.boundary_edges()))
print(m.faces)

f= m.faces[0]
print(m.face_vertices(f))

twin_count = sum(1 for he in m.halfedges if he.twin != None)
pairs = twin_count//2
print(pairs)
print(m.is_valid())
print(len(m.vertices_faces(m.vertices[2])))
print(m.is_2_manifold())

#round trip
m.to_obj()
test_path = os.path.join(script_dir,'..','data','cube_t0_obj_test.obj')
m2 = Mesh()
m2.build_from_obj(test_path)

assert len(m.vertices) == len(m2.vertices)
assert len(m.faces) == len(m2.faces)
assert len(m.halfedges) == len(m2.halfedges)
print('round trip success')