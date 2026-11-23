#marching_cubes
import numpy as np
from test_hausdorff import make_cube
import halfedge
from edge_flip import faces2idx, flip_cube
import mc_table as mc

CORNERS = [
    [0,0,0], [1,0,0], [1,1,0], [0,1,0],
    [0,0,1], [1,0,1], [1,1,1], [0,1,1],
]

EDGES = [
    (0, 1), (1, 2), (2, 3), (3, 0),     # 底面一圈   棱 0–3
    (4, 5), (5, 6), (6, 7), (7, 4),     # 顶面一圈   棱 4–7
    (0, 4), (1, 5), (2, 6), (3, 7),     # 四条竖边   棱 8–11
]

def marching_cubes_sample(iso =0.07):
    
    corner = CORNERS
    edges = EDGES

    values = [0, 1, 0, 0, 0, 0, 0, 0]

    return corner, edges, values, iso

def marching_cubes_sample_2in(iso =0.07):
    base = [0, 0, 0]

    corner = [
        [0,0,0], [1,0,0], [1,1,0], [0,1,0],
        [0,0,1], [1,0,1], [1,1,1], [0,1,1],
    ]

    edges = [
        (0, 1), (1, 2), (2, 3), (3, 0),     # 底面一圈   棱 0–3
        (4, 5), (5, 6), (6, 7), (7, 4),     # 顶面一圈   棱 4–7
        (0, 4), (1, 5), (2, 6), (3, 7),     # 四条竖边   棱 8–11
    ]

    values = [0, 1, 1, 0, 0, 0, 0, 0]

    return corner, edges, values, iso

def insert_p(corners, edges, values, iso):
    verts = []
    ts = []
    e_idx = []
    corners = np.array(corners)
    for idx, e in enumerate(edges):
        if (values[e[0]] >= iso) != (values[e[1]] >= iso):
            t = (iso - values[e[0]]) / (values[e[1]] - values[e[0]])
            vert = corners[e[0]] + t * (corners[e[1]] - corners[e[0]])
            verts.append(vert)
            ts.append(t)
            e_idx.append(idx)
    return verts, ts, e_idx

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

def cube_to_triangles(corners, edges, values, iso):
    inside = [values[k] >= iso for k in range(8)]
    idx = mc.cube_index(inside)
    tris = mc.triangles_of(idx)
    pts, ts , e_idx = insert_p(corners, edges, values, iso)
    by_edge = {e : p for e, p in zip(e_idx, pts)}

    return [tuple(by_edge[e] for e in tri) for tri in tris]

def sphere_surface_field(n = 33):
    c = np.linspace(-1.5, 1.5, n)
    dz, dy, dx = np.meshgrid(c, c, c, indexing='ij')
    data = np.sqrt(dx**2 + dy**2 + dz**2) - 1.0
    iso = 0.0

    return data, iso

def marching_cubes(data, iso):
    
    nz, ny, nx = data.shape
    verts = []
    faces = []

    for z in range(nz - 1):
        for y in range(ny - 1):
            for x in range(nx - 1):
                values = []
                corners = []
                for (cx, cy, cz) in CORNERS:
                    values.append(data[z + cz, y + cy, x + cx])
                    corners.append([x + cx, y + cy, z + cz])

                tris = cube_to_triangles(corners, EDGES, values, iso)

                for tri in tris:
                    i0 = len(verts)
                    verts.extend(tri)
                    faces.append((i0, i0 + 1, i0 + 2))

    return verts, faces