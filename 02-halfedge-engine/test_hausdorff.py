#hausdorff_test
import numpy as np, sys

import hausdorff as ha

def cube(h=1):
    verts = []
    for i in (h, -h):
        for j in (h, -h):
            for k in (h, -h):
                verts.append((i, j, k))

    faces = []
    for a in (0, 1, 2):
        for s in (-h, h):
            v = [0, 0, 0]
            p = (a+1) % 3
            q = (a+2) % 3
            v[a] = s
            v[p] = -s
            v[q] = -s
            v2 = v.copy()
            v2[p] = s
            v3 = v.copy()
            v3[q] = s
            v4 = v.copy()
            v4[p] = s
            v4[q] = s
            faces += [[v, v2, v3], [v2, v4, v3]]
    return np.array(verts), np.array(faces)

srf = np.array(((0,0,0), (2,0,0), (1,2,0)))
mesh2 = np.array((((0,0,0), (2,0,0), (1,2,0)), ((10,0,0), (12,0,0), (11,2,0))))
v1 = np.array((1, 1, 0))
v1s = ha.p_dis2surf(v1, srf)
v2 = np.array((1, 1, 3))
v2s = ha.p_dis2surf(v2, srf)
v3 = np.array((-1, -1, 0))
v3s = ha.p_dis2surf(v3, srf)
v4 = np.array((5, 5, 0))
v4s = ha.p_dis2surf(v4, srf)
v5 = np.array((1, 5, 0))
v5s = ha.p_dis2surf(v5, srf)
v6 = np.array((1, -3, 0))
v6s = ha.p_dis2surf(v6, srf)
v7 = np.array((2, 2, 0))
v7s = ha.p_dis2surf(v7, srf)
v8 = np.array((-1.5, 2, 0))
v8s = ha.p_dis2surf(v8, srf)

print(v1s,'\n', v2s,'\n', v3s,'\n', v4s,'\n', v5s,'\n', v6s,'\n', v7s,'\n', v8s)


def hausdroff():
    CASES1 = [
    (
        'verts',(v1, srf), 0.0
    ),
    (
        'verts',(v2, srf), 3.0
    ),
    (
        'verts',(v3, srf), 1.4142135624
    ),
    (
        'verts',(v4, srf), 5.0
    ),
    (
        'verts',(v5, srf), 3.0
    ),
    (
        'verts',(v6, srf), 3.0
    ),
    (
        'verts',(v7, srf), 0.8944271910
    ),
    (
        'verts',(v8, srf), 2.2360679775
    ),
    ]

    CASE2 = [
        (
        'DIS2MESH',(v1, mesh2), 0.0
    ),
        (
        'DIS2MESH',(np.array((11,1,0)), mesh2), 0.0
    ),
    ]

    CASE3 = [
        (
            'TEST_LMAX', srf, 2.2360679775
        ),
        (
            'TEST_LMAX', np.array(((0,0,0),(0.1,0,0),(10,0,0))) , 10.0
        ),
        (
            'TEST_LMAX', np.array(((0,0,0),(1,0,0),(0.5,0.8660254,0))), 1.0
        ),
        ]

    CASE4 = [
        (
            'hausdroff',((cube(0.5) + cube(1.5))), (1.0, 1.7320508, 1.4142136, 4.2426407, 5.9746915)
        )
    ]


    passed = 0
    total = 0
    for name, (verts, face), expected in CASES1:
        total += 1
        got = ha.p_dis2surf(verts, face)
        if abs(got - expected) <= 1e-6:
            print(f'{name}: PASS')
            passed += 1
        else:
            print(f'{name}: FAIL  expected {expected!r}, got {got!r}')

    for name, (verts, face), expected in CASE2:
        total += 1
        got = ha.p_dis2mesh(verts, face)
        if abs(got - expected) <= 1e-6:
            print(f'{name}: PASS')
            passed += 1
        else:
            print(f'{name}: FAIL  expected {expected!r}, got {got!r}')

    for name, tri, expected in CASE3:
        total += 1
        got = ha.l_max(tri)
        if abs(got - expected) <= 1e-6:
            print(f'{name}: PASS')
            passed += 1
        else:
            print(f'{name}: FAIL  expected {expected!r}, got {got!r}')

    for name, cubes, expected in CASE4:
        got = ha.hausdorff(*cubes)
        n = len(expected)
        for i in range(n):
            total += 1
            if np.abs(got[i] - expected[i]) <= 1e-6:
                print(f'{name}: PASS')
                passed += 1
            else:
                print(f'{name}: FAIL  expected {expected!r}, got {got!r}')

    return passed, total


p, n = hausdroff()
print(f'{p} passed, {n-p} failed')
sys.exit(0 if p == n else 1)