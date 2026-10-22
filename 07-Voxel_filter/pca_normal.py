#pca_normal
import numpy as np
import kdtree
# k from 10 to 100
#eigh select first column as normal vector

def compute_normals(points, k = 20):
    tree = kdtree.build(points)
    normal, eiglist = [], []
    for i in range(len(points)):
        idx = kdtree.kNN(tree, points, points[i], k)
        pts = points[idx]
        pts_cen = pts.mean(axis=0)
        X = pts - pts_cen
        H = X.T @ X
        eigvals, cov = np.linalg.eigh(H)
        normal.append(cov[:,0])
        eiglist.append(eigvals)
    return np.array(normal), np.array(eiglist)

#make plane
plane_xy = np.random.rand(1000, 2)
plane = np.column_stack([plane_xy, np.zeros(1000)])
normal_pl = np.array([0., 0., 1.])

#make sphere
r = 100
theta = np.random.uniform(0, np.pi, 1000)
phi = np.random.uniform(0, 2*np.pi, 1000)
x = r * np.sin(theta) * np.cos(phi)
y = r * np.sin(theta) * np.sin(phi)
z = r * np.cos(theta)
sphere = np.column_stack([x, y, z])
normal_sph = sphere / r

#make column
r_col = 1.0
theta_c = np.random.uniform(0, 2*np.pi, 1000)
x_col = r_col * np.cos(theta_c)
y_col = r_col * np.sin(theta_c)
z_col = np.random.rand(1000)
column = np.column_stack([x_col, y_col, z_col])
normal_col = np.column_stack([x_col/r_col, y_col/r_col, np.zeros(1000)])

n1, eigvals = compute_normals(plane)
dot = np.abs(np.sum(n1 * normal_pl, axis=1))
dot = np.clip(dot, 0.0, 1.0)
angle_deg = np.degrees(np.arccos(dot))
mean_angle = angle_deg.mean()

lam0, lam1, lam2 = eigvals[0], eigvals[1], eigvals[2]
linearity = (lam2 - lam1) / lam2
planarity = (lam1 - lam0) / lam2
scattering = lam0 / lam2
print(mean_angle)

plane_noisy = plane + np.random.normal(0, 0.01, plane.shape)
sphere_noisy = sphere + np.random.normal(0, 0.01, sphere.shape)
column_noisy = column + np.random.normal(0, 0.01, column.shape)

for k in [5, 10, 20, 50, 100, 200]:
    n1, _ = compute_normals(plane_noisy, k=k)
    dot = np.clip(np.abs(np.sum(n1 * normal_pl, axis=1)), 0.0, 1.0)
    err = np.degrees(np.arccos(dot)).mean()
    print(f"k={k:3d}  mean_angle={err:.4f}°")

for name, pts, gt in [('sphere', sphere, normal_sph),
                      ('column', column, normal_col)]:
    print(name)
    for k in [5, 10, 20, 50, 100, 200]:
        n1, _ = compute_normals(pts, k=k)
        dot = np.clip(np.abs(np.sum(n1 * gt, axis=1)), 0.0, 1.0)
        err = np.degrees(np.arccos(dot)).mean()
        print(f'k={k:3d} mean_angle={err:.4f}°')

for name, pts, gt in [('sphere_noisy', sphere_noisy, normal_sph),
                      ('column_noisy', column_noisy, normal_col)]:
    print(name)
    for k in [5, 10, 20, 50, 100, 200]:
        n1, _ = compute_normals(pts, k=k)
        dot = np.clip(np.abs(np.sum(n1 * gt, axis=1)), 0.0, 1.0)
        err = np.degrees(np.arccos(dot)).mean()
        print(f'k={k:3d} mean_angle={err:.4f}°')

import os
import laspy
scr_path = os.path.dirname(__file__)
data_path = os.path.join(scr_path, '..', 'data', 'small_dutch.laz')

with laspy.open(data_path) as f:
    las = f.read()
    N = 50000
    idx = np.linspace(0, len(las.xyz) - 1, N).astype(int)
    pts = las.xyz[idx]
    cls = las.classification[idx]
    print(np.unique(cls, return_counts=True))

    n1, eiglist = compute_normals(pts)
    lam0, lam1, lam2 = eiglist[:, 0], eiglist[:, 1], eiglist[:, 2]
    linearity = (lam2 - lam1) / lam2
    planarity = (lam1 - lam0) / lam2
    scattering = lam0 / lam2

    roof_med = np.median(planarity[cls == 6])
    veg_med  = np.median(planarity[(cls >= 3) & (cls <= 5)])

    print(f'roof planarity median={roof_med:.4f}, veg planarity median={veg_med:.4f}')