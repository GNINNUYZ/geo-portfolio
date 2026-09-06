#Ransac
import os
import laspy
import numpy as np

scr_path = os.path.dirname(__file__)
data_path = os.path.join(scr_path, '..', 'data', 'small_dutch.laz')

with laspy.open(data_path) as f:
    las = f.read()
    pts = las.xyz

    max_iter = 100

    def ransac(max_iter, threshold):
        best_count = 0
        best = None
        for i in range(max_iter):
            idx = np.random.choice(len(pts), 3, replace=False)
            sample = pts[idx]
            v1 = sample[1] - sample[0]
            v2 = sample[2] - sample[0]
            normal = np.cross(v1, v2)
            norm = np.linalg.norm(normal)
            if norm == 0:
                continue
            normal = normal / norm

            dist = np.abs(np.dot(pts - sample[0], normal))
            inliers = dist <= threshold
            count = inliers.sum()
            if count > best_count:
                best_count = count
                best = (normal, sample[0], inliers)
        return best

    def refine_plane(points, inliers):
        pts_in= points[inliers]
        centroid = pts_in.mean(axis=0)
        X = pts_in - centroid
        cov = X.T @ X
        _, Vt = np.linalg.eigh(cov)
        normal = Vt[:, 0]
        d = -normal @ centroid
        return normal, d

    plane = ransac(100, 0.1)
    normal, p1, inliers = plane
    refined = refine_plane(pts, inliers)
    print(inliers.sum())
    print(refined)

    np.random.seed(42)
    N = 1000

    xy = np.random.uniform(-10, 10, (N, 2))
    z1 = 2 * xy[:, 0] - 3 * xy[:, 1] + 5
    pts = np.column_stack([xy, z1])

    pts += np.random.normal(0, 0.1, (N, 3))

    n_out = int(N * 0.3)
    outliers = np.random.uniform(-10, 10, (n_out, 3))
    pts = np.vstack([pts, outliers])

    plane = ransac(100, 0.02)
    normal, p1, inliers = plane
    refined = refine_plane(pts, inliers)
    n1, d1 = refined
    n1 = n1 / np.linalg.norm(n1)
    true_normal = np.array([2, -3, -1])
    true_normal = true_normal / np.linalg.norm(true_normal)
    cos_ang = np.abs(n1 @ true_normal)
    cos_ang = np.clip(cos_ang, 0, 1)
    angle_deg = np.degrees(np.arccos(cos_ang))
    print(inliers.sum())
    print(refined)
    print(angle_deg)