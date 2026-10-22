#SHOT
import numpy as np
import kdtree
import orientation as ori


def lrf(pts, k = 20):
    tree = kdtree.build(pts)
    n = len(pts)
    out = np.empty((n, 3, 3))
    for i in range(n):
        #for p
        near_idx =[j for j in kdtree.kNN(tree, pts, pts[i], k) if j != i]
        near_dis = np.linalg.norm((pts[near_idx] - pts[i]), axis=1)
        dis_max = np.max(near_dis)
        w = dis_max - near_dis
        m_sum = np.zeros((3,3))
        w_sum = w.sum()
        for pos, j in enumerate(near_idx):
            X = pts[j] - pts[i]
            H = np.outer(X, X)
            M = (1 / w_sum) * w[pos] * H
            m_sum += M

        #eign m,get axis
        vals, norm = np.linalg.eigh(m_sum)
        z_axis = norm[:, 0]
        x_axis = norm[:, 1]
        
        # order norm:x
        d = np.dot((pts[near_idx] - pts[i]), x_axis)
        s = np.sign(d).sum()
        x_axis = x_axis * np.where(s < 0, -1.0, 1.0)
        # order norm:z
        d = np.dot((pts[near_idx] - pts[i]), z_axis)
        s = np.sign(d).sum()
        z_axis = z_axis * np.where(s < 0, -1.0, 1.0)
        # order norm:y
        y_axis = np.cross(z_axis, x_axis)

        R = np.column_stack([x_axis, y_axis, z_axis])
        out[i] = R
    return out

#32 branch
def shot(pts, k=20):
    N = len(pts)
    tree = kdtree.build(pts)
    L = lrf(pts, k)
    norm, _ = ori.compute_normals(pts, 20)
    norm = ori.orient_mst(pts, norm)
    F = np.zeros((N, 32 * 11))

    #p neibougher, axis:
    for i in range(N):
        near_idx = [j for j in kdtree.kNN(tree, pts, pts[i], k) if j != i]
        if len(near_idx) < 3:
            continue
        x, y, z = L[i][:, 0], L[i][:, 1], L[i][:, 2]
        v = pts[near_idx] - pts[i] #(N,3)
        near_dis = np.linalg.norm((pts[near_idx] - pts[i]), axis=1)
        dis_max = np.max(near_dis)
        v_x = v @ x
        v_y = v @ y
        v_z = v @ z
        theta = np.arctan2(v_y, v_x)
        theta_bin = np.clip(np.floor((theta + np.pi) / (2 * np.pi / 8)).astype(int), 0, 7)
        phi_bin = (v_z >= 0).astype(int)
        radius_bin = (near_dis >= dis_max / 2).astype(int)
        pid = theta_bin * 1 + phi_bin * 8 + radius_bin * 16

        cosT = norm[near_idx] @ z
        cbin = np.clip(np.floor((cosT + 1) / 2 * 11).astype(int), 0, 10)
        for pos, j in enumerate(near_idx):
            Fidx = pid[pos] * 11 + cbin[pos]
            F[i, Fidx] += 1
    f_sum = F.sum(axis=1, keepdims=True)
    f_sum[f_sum==0] = 1.0
    F = F / f_sum
    return F