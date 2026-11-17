import numpy as np
import halfedge
import os
from test_hausdorff import make_cube

script_dir = os.path.dirname(__file__)
data_dir = os.path.join(script_dir,'..','data','cube.obj')

verts, faces = make_cube(1)

m = halfedge.Mesh()
m.build_from_arrays(verts, faces)
hes = m.halfedges
for he in hes:
    if he.twin is not None:
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
