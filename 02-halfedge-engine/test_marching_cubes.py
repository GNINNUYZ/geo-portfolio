#test_marching_cubes
import numpy as np
from test_hausdorff import make_cube
from edge_flip import faces2idx, flip_cube
import marching_cubes as mc
import sys

def test_marching_cubes():
    c, e, v, i = mc.marching_cubes_sample() #corners, edges, values, iso
    pts, ts = mc.insert_p(c, e, v, i)

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
    return passed, total

if __name__ == '__main__':
    p, n = test_marching_cubes()
    print(f'{p} passed, {n-p} failed')
    sys.exit(0 if p == n else 1)
