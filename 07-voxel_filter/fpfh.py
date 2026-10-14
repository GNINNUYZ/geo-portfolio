import os
import laspy
import numpy as np
import kdtree
from orientation import compute_normals, orient_mst

scr_path = os.path.dirname(__file__)
data_path = os.path.join(scr_path, '..', 'data', 'small_dutch.laz')
with laspy.open(data_path) as f:
    las = f.read()
    pts = las.xyz
    idx = np.arange(len(pts))
    tree = kdtree.build(pts)
#KNN
    k = 5
    # 法向 + 全局定向：改用 orientation.py（不再自己算 → 上次那 3 个 bug 永久消失）
    normal, _ = compute_normals(pts, k=20)
    oriented = orient_mst(pts, normal)
    for i in idx:
        #对每个点，找到周围k个点
        sur_idx = kdtree.kNN(tree, pts, pts[i], k)
        matrix_pts = pts[np.array(sur_idx)]

        u = oriented[i]

        #PCH
        local_count = len(matrix_pts)
        v = np.cross((matrix_pts - pts[i]), u)
        w = np.cross(u, v)
        n_sur = oriented[sur_idx]
        
        #算特征值，u，v，w，alpha，phi，theta   
        alpha = v @ n_sur
        phi = u @ matrix_pts / np.abs(matrix_pts - pts[i].sum(), axis=1)
        sigma = np.arctan(w @ n_sur, u @ n_sur)

        #alpha,phi,theta,每个取值范围切成11个格子，对每个点看落在第几个，形成3 * 11维后归一化（除以总计数k）
        alpha_bin = np.floor(((1 + alpha) / 2) * 11)
        phi_bin = np.floor(((1 + phi) / 2) * 11)
        sigma_bin = np.floor(((sigma) / (np.pi/3)) * 11)

        charac_matrix = np.column_stack((alpha_bin, phi_bin, sigma_bin), axis=0)
        charac_stand = charac_matrix / k
        
        #取 p 的 k 个邻居已经算好的 SPFH，按 1/ω 加权、除以 k 求平均，然后加到 p 自己的 SPFH 上；其中 ω = p 到那个邻居的距离。
        sur_len = np.abs((pts[i] - matrix_pts).sum(), axis=1)
        pfh = np.column_stack((u, v, w), axis=0)
        spfh = pfh + (np.dot(((1 / sur_len) * charac_stand), axis=1) / k)
