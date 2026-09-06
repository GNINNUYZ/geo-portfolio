# 07 - Point Cloud Toolbox (Voxel Filter / KD-tree / RANSAC / ICP)

Hand-written point cloud algorithms in Python, tested on a real Dutch airborne point cloud (`small_dutch.laz`).

## Features

- **Voxel filter**: downsample a point cloud with `mean` / `first` / `median` representative modes.
- **KD-tree**: 3D KD-tree with kNN and radius search, verified against brute force.
- **RANSAC**: robust plane fitting (random sampling + optional SVD refinement).
- **ICP**: point-to-point registration via SVD, with configurable initial pose.
- **Edge-case handling**: empty clouds, single points, identical points, large voxels.

## Files

| File | Description |
|---|---|
| `voxel_filter.py` | Voxel downsampling (`mean` / `first` / `median`) |
| `kdtree.py` | KD-tree build + kNN + radius search + brute-force verification |
| `ransac_plane.py` | RANSAC plane fitting on real point cloud |
| `icp.py` | Point-to-point ICP with initial pose support |
| `voxel.centroids.npy` | Example voxel filter output |

## Requirements

`laspy`, `numpy`

## Usage

```bash
python voxel_filter.py
python kdtree.py
python ransac_plane.py
python icp.py
```

Data path: `../data/small_dutch.laz`

## Results

### Voxel filter (voxel_size = 1.0 m)

- Original points: 1,000,000
- Voxels: 204,394
- Compression rate: 20.4%

### KD-tree kNN benchmark (k = 5, 100 queries)

| N | KD-tree | Brute force | Speedup |
|---|---|---|---|
| 1k | 0.0298 s | 0.0040 s | 0.1x |
| 10k | 0.0376 s | 0.0248 s | 0.7x |
| 100k | 0.0443 s | 0.3901 s | 8.8x |

Conclusion: brute force is faster below ~10k points; KD-tree becomes clearly faster at 100k+.

### ICP initial-pose test (synthetic data, micro noise)

| Initial pose | R error | t error |
|---|---|---|
| 0.0° | 6.06e-15 | 1.61e-14 |
| 5.7° | 1.86e-15 | 1.24e-14 |
| 17.2° | 2.35e-15 | 7.44e-15 |
| 34.4° | 4.39e-15 | 2.37e-14 |
| 57.3° | 3.09e-15 | 2.84e-14 |

### Edge cases

All passed: empty cloud, single point, identical points, large voxel, fewer than 3 points for RANSAC.

