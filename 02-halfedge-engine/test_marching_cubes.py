#test_marching_cubes
import numpy as np
from test_hausdorff import make_cube
from edge_flip import faces2idx, flip_cube
import marching_cubes as mc
import sys
import mc_table

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
    for i, t in enumerate(tri_p):
        normal = np.cross((t[1] - t[0]), (t[2] - t[0]))
        normal = normal /np.linalg.norm(normal)
        normals.append(normal)

    for j, n in enumerate(normals):
        total += 1
        if n @ (np.array(tri_p[j]).mean(axis=0) - cube_cen) > 0:
            passed += 1


    return passed, total


value1 = [0, 1, 0, 0, 0, 0, 0, 0]
value2 = [0, 1, 1, 0, 0, 0, 0, 0]

if __name__ == '__main__':
    p, n = test_marching_cubes()
    print(f'{p} passed, {n-p} failed')
    sys.exit(0 if p == n else 1)