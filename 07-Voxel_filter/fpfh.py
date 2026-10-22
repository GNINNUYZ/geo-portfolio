import os
import laspy
import numpy as np
import kdtree
from orientation import compute_normals, orient_mst

def hist(vals, lo, hi):
    vals = vals[np.isfinite(vals)]
    t = (vals - lo) / (hi - lo)
    b = np.clip(np.floor(t * 11).astype(np.int64), 0, 10)
    h = np.zeros(11)
    np.add.at(h, b, 1.00)
    return h / h.sum()
    

def compute_fpfh(pts, k=5):
    idx = np.arange(len(pts))
    tree = kdtree.build(pts)
#KNN
    # 法向 + 全局定向
    normal, _ = compute_normals(pts, k)
    oriented = orient_mst(pts, normal)
    spfh_all = []
    for i in idx:
        #对每个点，找到周围k个点
        sur_idx = [j for j in kdtree.kNN(tree, pts, pts[i], k) if j != i]
        matrix_pts = pts[np.array(sur_idx)]

        u = oriented[i]
        #PCH
        local_count = len(matrix_pts)
        v = np.cross((matrix_pts - pts[i]), u)
        v /= (np.linalg.norm(v, axis=1, keepdims=True) + 1e-12)
        w = np.cross(u, v)
        n_sur = oriented[sur_idx]
        
        #算特征值，u，v，w，alpha，phi，theta   
        alpha = (v * n_sur).sum(axis=1)
        d = np.linalg.norm(matrix_pts - pts[i], axis=1)
        phi = (u * (matrix_pts - pts[i])).sum(axis=1) / d
        sigma = np.arctan2((w * n_sur).sum(axis=1), (u * n_sur).sum(axis=1))

        #alpha,phi,theta,每个取值范围切成11个格子，对每个点看落在第几个，形成3 * 11维后归一化（除以总计数k
        alpha_bin = hist(alpha, -1.0, 1.0)
        phi_bin = hist(phi, -1.0, 1.0)
        sigma_bin = hist(sigma, -np.pi/3, np.pi/3)
        spfh_all.append(np.concatenate([alpha_bin, phi_bin, sigma_bin]))

    spfh_all = np.asarray(spfh_all)
    fpfh = np.empty_like(spfh_all)

    #取 p 的 k 个邻居已经算好的 SPFH，按 1/ω 加权、除以 k 求平均，然后加到 p 自己的 SPFH 上；其中 ω = p 到那个邻居的距离。
    for i in idx:
        sur_idx = np.array([j for j in kdtree.kNN(tree, pts, pts[i], k) if j != i])
        dd = np.linalg.norm(pts[sur_idx] - pts[i], axis=1) + 1e-12
        fpfh[i] = spfh_all[i] + (spfh_all[sur_idx] / dd[:, None]).sum(axis=0) / k
    
    return fpfh

if __name__ == '__main__':
    scr_path = os.path.dirname(__file__)
    data_path = os.path.join(scr_path, '..', 'data', 'small_dutch.laz')
    with laspy.open(data_path) as f:
        las = f.read()
        pts = las.xyz
        pts = pts[::50]
        compute_fpfh(pts)