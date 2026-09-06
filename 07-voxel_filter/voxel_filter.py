#体素滤波
import laspy
import os
import numpy as np


def voxel_filter(points, voxel_size=1.0):
    if len(points) == 0:
        return np.zeros((0, 3))

    mins = points.min(axis=0)
    voxel_xyz = np.floor((points - mins) / voxel_size).astype(np.int64)
    _, inverse = np.unique(voxel_xyz, axis=0, return_inverse=True)
    # inverse, add.at
    n_voxels = inverse.max() + 1
    sums = np.zeros((n_voxels, 3))
    np.add.at(sums, inverse, points)
    #bincount
    counts = np.bincount(inverse)
    centroids = sums / counts[:, None]

    return centroids

if __name__ == '__main__':
    import laspy
    import os

    scr_path = os.path.dirname(__file__)
    data_path = os.path.join(scr_path,'..', 'data', 'small_dutch.laz')

    with laspy.open(data_path) as f:
        las = f.read()
    pts = las.xyz

    centroids = voxel_filter(pts, 1.0)

    print('压缩率：{:.1f}%'.format(100 * n_voxels / las.xyz.shape[0]))

    out_path = os.path.join(scr_path, 'voxel.centroids.npy')
    np.save(out_path, centroids)
    print('already saved:', out_path)