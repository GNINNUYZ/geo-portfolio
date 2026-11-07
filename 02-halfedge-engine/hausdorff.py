#hausdorff
import numpy as np

pts = np.array((-1.5, 2, 0))
srf = np.array(((0,0,0),(2,0,0),(1,2,0)))

def p_dis2surf(pts, srf):
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

def p_dis2mesh(pts, mesh):
    dis_mesh = []

    for f in mesh:
        dis = p_dis2surf(pts, f)
        dis_mesh.append(dis)
    return np.array(dis_mesh).min()

def l_max(srf):
    n = len(srf)
    l1 = np.arange(n)
    l2 = np.append(l1[1:], l1[0])
    l_dis = []
    for i, j in zip(l1, l2):
        l_dis.append(np.linalg.norm(srf[j] - srf[i]))
    return np.array(l_dis).max()


def hausdorff(v1,m1, v2,m2):
    dis1to2 = []
    for vert1 in v1:
        dis1to2.append(p_dis2mesh(vert1, m2))
    h1_collect = []
    for f1 in m1:
        h1 = l_max(f1)
        h1_collect.append(h1)
    d1max_idx = np.argmax(h1_collect)
    h1max = h1_collect[d1max_idx]

    dis2to1 = []
    for vert2 in v2:
        dis2to1.append(p_dis2mesh(vert2, m1))
    h2_collect = []
    for f2 in m2:
        h2 = l_max(f2)
        h2_collect.append(h2)
    d2max_idx = np.argmax(h2_collect)
    h2max = h2_collect[d2max_idx]

    d1max = np.array(dis1to2).max()
    d2max = np.array(dis2to1).max()
    H_upper = max(d1max + h1max, d2max + h2max)
    return d1max, d2max, h1max, h2max, H_upper
