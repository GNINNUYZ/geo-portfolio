#test_marching_cubes
import numpy as np
from test_hausdorff import make_cube
from edge_flip import faces2idx, flip_cube
import marching_cubes as mc
import sys
import mc_table
import halfedge

corner = [
    [0,0,0], [1,0,0], [1,1,0], [0,1,0],
    [0,0,1], [1,0,1], [1,1,1], [0,1,1],
]

edges = [
    (0, 1), (1, 2), (2, 3), (3, 0),     # 底面一圈   棱 0–3
    (4, 5), (5, 6), (6, 7), (7, 4),     # 顶面一圈   棱 4–7
    (0, 4), (1, 5), (2, 6), (3, 7),     # 四条竖边   棱 8–11
]

values = [0, 1, 0, 0, 0, 0, 0, 0]

def test_marching_cubes():
    c, e, v, i = mc.marching_cubes_sample() #corners, edges, values, iso
    pts, ts, _ = mc.insert_p(c, e, v, i)

    total = 0
    passed = 0

    total += 1
    if len(pts) == 3:
        passed += 1

    total += 1
    if {tuple(round(float(x), 6) for x in p) for p in pts} == {(0.07,0,0), (1,0.93,0), (1,0,0.93)}:
        passed += 1

    total += 1
    tn = len(ts)
    tpass = 0
    for t in ts:
        if 0 <= t <=1 :
            tpass += 1
    if tpass == tn:
        passed += 1

    c, e, v, i = mc.marching_cubes_sample_2in() #corners, edges, values, iso

    c = np.array(c)
    tri_p = mc.cube_to_triangles(c, e, v, i)

    total += 1
    if len(tri_p) == 2:
        passed += 1

    cube_cen = np.array(c).mean(axis=0)
    normals = []
    for id3, t in tri_p:
        normal = np.cross((id3[1] - id3[0]), (id3[2] - id3[0]))
        normal = normal /np.linalg.norm(normal)
        normals.append(normal)

    for j, n in enumerate(normals):
        total += 1
        if n @ (np.array(tri_p[j][0]).mean(axis=0) - cube_cen) > 0:
            passed += 1

    for k in range(8):
        idx  = mc_table.cube_index([j == k for j in range(8)])
        tris = mc_table.triangles_of(idx)
        want = [e for e, (a, b) in enumerate(edges) if k in (a, b)]

        total += 1
        if len(tris) == 1:
            passed += 1

        total += 1
        if set(tris[0]) == set(want):
            passed += 1

    data, iso, cspace = mc.sphere_surface_field()
    vs, fs = mc.marching_cubes(data, iso, cspace)
    
    m = halfedge.Mesh()
    m.build_from_arrays(np.array(vs), fs)

    V = len(m.vertices)
    E = len(m.halfedges) // 2
    F = len(m.faces)

    chi = V - E + F

    total += 1
    if chi == 2:
        passed += 1
    
    total += 1
    if len(m.boundary_edges()) == 0:
        passed += 1

    total += 1
    valid_he = 0
    for he in m.halfedges:
        if he.twin.twin is he:
            valid_he += 1
    if valid_he == len(m.halfedges):
        passed += 1

    total += 1
    valid_p = 0
    for p in np.array((vs)):
        if abs(np.linalg.norm(p) - 1) < 1e-2:
            valid_p += 1
    if valid_p == len(m.vertices):
        passed += 1

    total += 1
    fs_area = 0
    for f in fs:
        f_area = 0.5 * np.linalg.norm(np.cross((vs[f[1]] - vs[f[0]]), (vs[f[2]] - vs[f[0]])))
        fs_area += f_area

    if abs(fs_area - (4*np.pi)) / (4*np.pi) <= 0.01:
        passed += 1

    return passed, total


value1 = [0, 1, 0, 0, 0, 0, 0, 0]
value2 = [0, 1, 1, 0, 0, 0, 0, 0]

if __name__ == '__main__':
    p, n = test_marching_cubes()
    print(f'{p} passed, {n-p} failed')
    sys.exit(0 if p == n else 1)