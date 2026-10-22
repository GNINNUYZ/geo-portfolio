#ICP
import numpy as np
import os
import laspy
import time
from kdtree import build, kNN
from voxel_filter import voxel_filter


def icp(src, dst, max_iter=50, tol=1e-6):
    R = np.eye(3)
    t = np.zeros(3)
    prev_error = float('inf')
    t1 = time.time()
    for i in range(max_iter):
        src_trans = src @ R.T + t
        pts = dst

        #nearest point
        near_idx = []
        tree = build(dst)

        for q in src_trans:
            near_idx.append(kNN(tree, dst, q, 1)[0])
        near_pts = dst[near_idx]

        #center
        near_pts = pts[np.array(near_idx)]
        src_c = src_trans.mean(axis = 0)
        near_c = near_pts.mean(axis = 0)

        #cov
        src_cen = src_trans - src_c
        near_cen = near_pts - near_c
        H = src_cen.T @ near_cen / len(src_trans)

        #SVD
        U, S, Vt = np.linalg.svd(H)
        dR = Vt.T @ U.T
        if np.linalg.det(dR) < 0:
            U[:, -1] *= -1
            dR = Vt.T @ U.T
        dt = near_c - dR @ src_c

        R = dR @ R
        t = t @ dR.T  + dt

        #error
        error = np.sqrt(np.mean(((src @ R.T + t - near_pts) ** 2)))
        if abs((prev_error - error)/prev_error) < tol:
            break
        prev_error = error
    t2 = time.time()
    t_use = t2 -t1
    return R, t, i, t_use, error

src = np.random.rand(1000, 3) * 10

true_R = np.array([[np.cos(0.3), -np.sin(0.3), 0],
        [np.sin(0.3),  np.cos(0.3), 0],
        [0, 0, 1]])
true_t = np.array([1, 2, 3])
dst = src @ true_R.T + true_t

R, t, _, _, _= icp(src, dst)

print("R error:", np.linalg.norm(R - true_R))
print('t error:', np.linalg.norm(t - true_t))

scr_path = os.path.dirname(__file__)
data_path = os.path.join(scr_path,'..','data','small_dutch.laz')
with laspy.open(data_path) as f:
    las = f.read()

pts = las.xyz

mask = ((pts[:, 0] > pts[:, 0].min() + 5) & (pts[:, 0] < pts[:, 0] + 30) &
        (pts[:, 1] > pts[:, 1].min() + 5) & (pts[:, 1] < pts[:, 1] + 30))
crop = pts[mask]
crop, _ = voxel_filter(crop, 1.0)

angle = 0.2
true_R = np.array([[np.cos(angle), -np.sin(angle), 0],
        [np.sin(angle),  np.cos(angle), 0],
        [0, 0, 1]])
true_t = np.array([1.0, 2.0, 0.5])

src = crop
dst = crop @ true_R.T + true_t

R, t, i, t_use, error = icp(src, dst)

print("R error:", np.linalg.norm(R - true_R))
print('t error:', np.linalg.norm(t - true_t))
print(f'end after {i} iter:')
print('time use:', t_use)
print('error:', error)