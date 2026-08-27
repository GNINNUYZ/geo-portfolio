#体素滤波
import laspy
import os
import numpy as np

scr_path = os.path.dirname(__file__)
data_path = os.path.join(scr_path,'..', 'data', 'small_dutch.laz')

with laspy.open(data_path) as f:
    las = f.read()
    x_min = las.header.mins[0]
    y_min = las.header.mins[1]
    z_min = las.header.mins[2]

    x_max = las.header.maxs[0]
    y_max = las.header.maxs[1]
    z_max = las.header.maxs[2]

    voxel_size = 1.0

    bbox_xrange = np.arange(x_min, x_max, voxel_size)
    bbox_yrange = np.arange(y_min, y_max, voxel_size)
    bbox_zrange = np.arange(z_min, z_max, voxel_size)

    print (bbox_xrange)
    #floor
    voxel_x = np.floor((las.x - x_min) / voxel_size).astype(int)
    voxel_y = np.floor((las.y - y_min) / voxel_size).astype(int)
    voxel_z = np.floor((las.z - z_min) / voxel_size).astype(int)
    #unique
    voxel_ids= np.stack([voxel_x, voxel_y, voxel_z], axis=1)
    _, inverse = np.unique(voxel_ids, axis=0, return_inverse=True)
    # inverse, add.at
    n_voxels = inverse.max() + 1
    sums = np.zeros((n_voxels, 3))
    np.add.at(sums, inverse, las.xyz)
    #bincount
    counts = np.bincount(inverse)
    centroids = sums / counts[:, None]

    print('压缩率：{:.1f}%'.format(100 * n_voxels / las.xyz.shape[0]))

    out_path = os.path.join(scr_path, 'voxel.centroids.npy')
    np.save(out_path, centroids)
    print('already saved:', out_path)