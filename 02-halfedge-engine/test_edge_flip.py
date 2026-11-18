#test_edge_flip
import numpy as np, sys
import halfedge
import os
from test_hausdorff import make_cube
from edge_flip import faces2idx, flip_cube

verts, faces = make_cube(1)
m = halfedge.Mesh()
verts, faces_idx = faces2idx(verts, faces)
m.build_from_arrays(verts, faces_idx)

def test_edge_flip():
    CASE0 = [
        'Test edgeflip', flip_cube(m), 
    ]