import numpy as np
import halfedge
import os
from test_hausdorff import make_cube

script_dir = os.path.dirname(__file__)
data_dir = os.path.join(script_dir,'..','data','cube.obj')

verts, faces = make_cube(1)
lookup = {tuple(v) : i for i, v in enumerate(verts)}
faces_idx = np.zeros((len(faces),3), dtype=int)
for c, f in enumerate(faces):
    for j, p in enumerate(f):
        faces_idx[c][j] = lookup[tuple(p)]


m = halfedge.Mesh()
m.build_from_arrays(verts, faces_idx)
hes = m.halfedges
count = 0
for he in hes:

    if he.twin is not None:
        n = (he.origin.x != he.twin.origin.x) + (he.origin.y != he.twin.origin.y) + (he.origin.z != he.twin.origin.z)

        if n != 2:
            continue
        count += 1
        f1 = he.face

        he2 = he.twin
        f2 = he2.face
        
        h_ab = he.prev
        h_ca = he.next
        h_bd = he2.next
        h_dc = he2.prev
        a = h_ab.origin
        d = h_dc.origin

        h_ab.next = h_bd
        h_dc.next = h_ca
        he.origin = d
        he2.origin = a
        h_bd.next = he
        h_ca.next = he2
        he.next = h_ab
        he2.next = h_dc

        h_ab.prev = he
        h_bd.prev = h_ab
        he.prev = h_bd
        he2.prev = h_ca
        h_ca.prev = h_dc
        h_dc.prev = he2

        h_bd.face = f1
        h_ca.face = f2
        if count == 1:
            break
