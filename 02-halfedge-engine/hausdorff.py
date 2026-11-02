#hausdorff
import numpy as np

pts = np.array((1, 1, 1))
srf = np.array(((1, 0, 0),(0, 1, 0),(0, 0, 1)))

def p_proj(pts, srf):
    v_ca = srf[2] - srf[0]
    v_ba = srf[1] - srf[0]
    v_bc = srf[2] - srf[1]
    A = np.vstack((v_ba, v_ca))

    x = np.linalg.solve(A @ A.T, A @ (pts - srf[0]))

    pproj = srf[0] + x[0] * v_ba + x[1] * v_ca

    v = x[0]
    w = x[1]

    dis = 0
    
    if v >= 0 & w >=0 & v + w <= 1:
        dis = 0

    if v >= 0 & w >=0 & v + w > 1:
        v_bp = pproj - srf[1]
        cos_theta = np.dot(v_bp, v_bc) / np.linalg.norm(v_bp)*np.linalg.norm(v_bc)
        t =  np.linalg.norm(v_bp * cos_theta) / np.linalg.norm(v_bc)
        if t < 1:
            dis = np.linalg.norm(v_bp - v_bc * t)
        else:
            dis = np.linalg.norm(pproj - srf[2])


