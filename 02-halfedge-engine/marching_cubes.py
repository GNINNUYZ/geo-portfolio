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
