# 07 - Voxel Filter & KD-tree

Point cloud downsampling and nearest-neighbor search tools, tested on a real Dutch airborne point cloud (`small_dutch.laz`).

## Features

- **Voxel filter**: downsample a point cloud by grouping points into 3D voxels and keeping one representative point (centroid) per voxel.
- **KD-tree**: build a 3D KD-tree, supporting k-nearest-neighbor (kNN) and radius search.
- **Brute-force comparison**: verify the tree-based kNN against a numpy brute-force implementation and compare runtime.

## Files

| File | Description |
|---|---|
| `voxel_filter.py` | Voxel filter implementation (LAZ -> centroid points) |
| `kdtree.py` | KD-tree construction + kNN + radius search + brute-force verification |
| `voxel.centroids.npy` | Voxel filter output (centroid points) |

## Requirements

`laspy`, `numpy`

## Usage

```bash
python voxel_filter.py
python kdtree.py
```

Data path: `../data/small_dutch.laz`

## Results

Voxel filter (voxel_size = 1.0 m):

- Original points: 1,000,000
- Voxels: 204,394
- Compression rate: 20.4%

KD-tree kNN (100 queries, k = 5):

| Method | Time |
|---|---|
| Brute force (numpy) | 2.1307 s |
| KD-tree (Python) | 0.9709 s |
| Speedup | 2.2x |

