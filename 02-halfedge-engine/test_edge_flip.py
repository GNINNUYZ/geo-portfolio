#test_edge_flip
import numpy as np, sys
import halfedge
import os
from test_hausdorff import make_cube
from edge_flip import faces2idx, flip_cube

def fresh():
    verts, faces = make_cube(1)
    m = halfedge.Mesh()
    verts, faces_idx = faces2idx(verts, faces)
    m.build_from_arrays(verts, faces_idx)
    return m


def edge_num_calc():
    m = fresh()
    edgemap = dict()
    for i, v in enumerate(m.halfedges):
        sp = v.origin
        ep = v.next.origin
        edgemap[(sp, ep)] = i

    flip_cube(m)
    edgeflipmap = dict()
    for i, v in enumerate(m.halfedges):
        sp = v.origin
        ep = v.next.origin
        edgeflipmap[(sp, ep)] = i

    miss = 0
    add = 0
    for k in edgemap:
        if k  not in edgeflipmap:
            miss += 1
        
    for k in edgeflipmap:
        if k  not in edgemap:
            add += 1

    return miss, add

def edge_flip_2():
    m = fresh()
    edgemap = dict()
    for i, v in enumerate(m.halfedges):
        sp = v.origin
        ep = v.next.origin
        edgemap[(sp, ep)] = i

    flip_cube(m)
    flip_cube(m)
    edgeflipmap = dict()
    for i, v in enumerate(m.halfedges):
        sp = v.origin
        ep = v.next.origin
        edgeflipmap[(sp, ep)] = i

    miss = 0
    add = 0
    for k in edgemap:
        if k  not in edgeflipmap:
            miss += 1
        
    for k in edgeflipmap:
        if k  not in edgemap:
            add += 1

    return miss, add

def edge_attribute_check():
    m = fresh()
    flip_cube(m)
    total = 0
    passed = 0

    bad_edge_count = 0    
    total += 1
    for i in m.halfedges:
        if i.twin.twin != i:
            bad_edge_count += 1
    

    total += 1
    bad_faces = 0
    for f in m.faces:
        if f.halfedge.next.next.next != f.halfedge:
            bad_faces += 1

    total += 1
    bad_edge2face = 0
    for f in m.faces:
        if f.halfedge.face != f:
            bad_edge2face += 1

    total += 1
    passed += (bad_edge_count == 0) + (bad_faces == 0) + (bad_edge2face == 0)
    if len(m.boundary_edges()) == 0:
        passed += 1

    return passed, total


def test_edge_flip():
    m = fresh()
    before_v = len(m.vertices)
    before_e = len(m.halfedges) // 2
    before_f = len(m.faces)

    flip_cube(m)
    after_v = len(m.vertices)
    after_e = len(m.halfedges) // 2
    after_f = len(m.faces)

    passed = 0
    total = 0

    for i, j in zip ((before_v, before_e, before_f), (after_v, after_e, after_f)):
        total += 1
        if i == j:
            passed += 1

    miss, add = edge_num_calc()

    total += 1
    if miss == 2:
        passed += 1

    total += 1
    if add == 2:
        passed += 1

    miss, add = edge_flip_2()
    total += 1
    if miss == 0:
        passed += 1

    total += 1
    if add == 0:
        passed += 1

    p2, n2 = edge_attribute_check()
    passed += p2
    total += n2

    return passed, total


    

if __name__ == '__main__':
    p, n = test_edge_flip()
    print(f'{p} passed, {n-p} failed')
    sys.exit(0 if p == n else 1)