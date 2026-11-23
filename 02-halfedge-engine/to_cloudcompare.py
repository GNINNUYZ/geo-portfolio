#to_cloudcompare
import icosphere
import halfedge
import numpy as np
import os

script_dir = os.path.dirname(__file__)
data_dir = os.path.join(script_dir,'..','data','test00.obj')

verts, faces = icosphere.icosphere(sub=2)
m = halfedge.Mesh()
m.build_from_arrays(verts, faces)
m.to_obj(path=data_dir)