#main_curvature
import numpy as np
import icosphere

vs, faces = icosphere.icosphere()

def v2f(faces):
    v_fs = {}
    for fi, f in enumerate(faces):
        for v in f:
            v_fs.setdefault(v, []).append(fi)
    return v_fs

def curvature(verts, faces, v2fs):
    v_curvature = {}
    v_area = {}
    v_k = {}
    for v_key in v2fs:
        fs = v2fs[v_key]
        for fi in fs:
            f = faces[fi]
            i = f.index(v_key)
            i_prev = f[(i - 1) % 3]
            i_next = f[(i + 1) % 3]
            
            a = verts[i_prev] - verts[v_key]
            b = verts[i_next] - verts[v_key]

            f_area = 0.5 * np.linalg.norm(np.cross(a, b))
            cos_theta = (a @ b) / (np.linalg.norm(a) * np.linalg.norm(b))
            theta = np.arccos(cos_theta)

            if v_key not in v_curvature:
                v_curvature[v_key] = theta
            else:
                v_curvature[v_key] += theta

            if v_key not in v_area:
                v_area[v_key] = f_area / 3
            else:
                v_area[v_key] += f_area / 3
        
        k = (2 * np.pi - v_curvature[v_key]) / (v_area[v_key])
        v_k[v_key] = k
        
    return v_curvature, v_area, v_k