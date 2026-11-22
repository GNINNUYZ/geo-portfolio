#marching_cubes
import numpy as np
from test_hausdorff import make_cube
import halfedge
from edge_flip import faces2idx, flip_cube

def marching_cubes_sample(iso =0.07):
    base = [0, 0, 0]
    corner = []

    for i in range(2):
        a = base.copy()
        a[2] = i
        for j in range(2):
            a[1] = j
            for k in range(2):
                a[0] = k
                corner.append(a.copy())

    edges = [
        (0,1), (2,3), (4,5), (6,7),     # 沿 x
        (0,2), (1,3), (4,6), (5,7),     # 沿 y
        (0,4), (1,5), (2,6), (3,7),     # 沿 z
    ]

    values = [0, 1, 0, 0, 0, 0, 0, 0]

    return corner, edges, values, iso

def marching_cubes_sample_2in(iso =0.07):
    base = [0, 0, 0]
    corner = []

    for i in range(2):
        a = base.copy()
        a[2] = i
        for j in range(2):
            a[1] = j
            for k in range(2):
                a[0] = k
                corner.append(a.copy())

    edges = [
        (0,1), (2,3), (4,5), (6,7),     # 沿 x
        (0,2), (1,3), (4,6), (5,7),     # 沿 y
        (0,4), (1,5), (2,6), (3,7),     # 沿 z
    ]

    values = [0, 1, 0, 1, 0, 0, 0, 0]

    return corner, edges, values, iso

def insert_p(corners, edges, values, iso):
    verts = []
    ts = []
    corners = np.array(corners)
    for e in edges:
        if (values[e[0]] >= iso) != (values[e[1]] >= iso):
            t = (iso - values[e[0]]) / (values[e[1]] - values[e[0]])
            vert = corners[e[0]] + t * (corners[e[1]] - corners[e[0]])
            verts.append(vert)
            ts.append(t)
    return verts, ts

def srf_direction(corners, verts):    
    corners = np.array(corners)
    v = np.array(verts)

    cube_mid = corners.sum(axis=0) / len(corners)
    tri_mid = v.sum(axis=0) / len(v)

    
    def direct_tri_3pts(v):
        n1 = v[1] - v[0]
        n2 = v[2] - v[0]
        normal = np.cross(n1, n2)
        normal = normal/ np.linalg.norm(normal)

        if (normal @ (tri_mid - cube_mid)) < 0:
            normal *= -1
            new_v = (v[0], v[2], v[1])
        else:
            new_v = (v[0], v[1], v[2])
        return new_v, normal

    if len(v) == 3:
        new_v, normal = direct_tri_3pts((v))

    if len(v) == 4:
        tri1 = (v[0], v[1], v[2])
        tri2 = (v[0], v[2], v[3])
        tri1_new_v, normal1 = direct_tri_3pts(tri1)
        tri2_new_v, normal2 = direct_tri_3pts(tri2)

        new_v = (tri1_new_v, tri2_new_v)
        normal = (normal1, normal2)

    return new_v, normal