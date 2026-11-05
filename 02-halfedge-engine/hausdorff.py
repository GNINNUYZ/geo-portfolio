#hausdorff
import numpy as np

pts = np.array((-1.5, 2, 0))
srf = np.array(((0,0,0),(2,0,0),(1,2,0)))

def p_proj(pts, srf):
    v_ca = srf[2] - srf[0]
    v_ba = srf[1] - srf[0]
    A = np.vstack((v_ba, v_ca))

    x = np.linalg.solve(A @ A.T, A @ (pts - srf[0]))

    pproj = srf[0] + x[0] * v_ba + x[1] * v_ca

    v = x[0]
    w = x[1]
    
    dis_add = []

    if v >= 0 and w >=0 and v + w <= 1:
        dis = np.linalg.norm(pts - pproj)
        return dis

    for i, j in zip((0, 1, 2), (1, 2, 0)):

        v_op = pts - srf[i]
        v_oc = srf[j] - srf[i]
        t =  np.dot(v_op, v_oc) / (np.linalg.norm(v_oc) ** 2)
        if 0 < t < 1:
            dis = np.linalg.norm(pts - ((v_oc * t) + srf[i]))
        elif t >= 1:
            dis = np.linalg.norm(pts - srf[j])
        else:
            dis = np.linalg.norm(pts - srf[i])
        dis_add.append(dis)
        
    return np.array(dis_add).min()

print(p_proj(pts, srf))
