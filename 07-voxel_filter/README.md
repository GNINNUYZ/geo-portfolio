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

### BUG FIX history
1. L37 read 'n_voxels' name error.
n_voxel can not get parameters in modules branch, n_voxels get parameter in voxel_filter() function.
2. voxel_filter() return centroids, n_voxels 2 parameters.
3. find in L9 pre-return branch also need 2 paramaters.
4. recalculate need to voxel logic re-calculate.
5. need check all return parameters, not only the last one.

---

## PCA 法向估计 + 邻域尺度实验（M1）

`pca_normal.py` — 逐点法向估计 + 三个几何派生量 + 合成曲面上的邻域尺度实验（对应 Weinmann et al. 2015 §2.1 的「最优邻域」）。

### 方法（一句话）

每个点取 k 近邻 → 中心化 → 协方差 H = XᵀX → `eigh(H)` → **最小特征值方向 = 法向**（eigh 返回升序：λ0 ≤ λ1 ≤ λ2）。

三个派生量（升序特征值）：

```
线性度  linearity  = (λ2 − λ1) / λ2
平面度  planarity  = (λ1 − λ0) / λ2
散射度  scattering = λ0 / λ2
```

### 合成曲面结果（各 1000 点，真值法向已知）

| 曲面 | 参数 | 曲率 | U 形 | 最优 k | 最优误差 |
|---|---|---|---|---|---|
| 平面 | z=0 | 0 | 无（单调下降） | — | 0.0°（无噪声） |
| 球 | r=100 | 0.01 | 浅 U | 【填】 | 【填】 |
| 柱 | r=1 | 1 | 深 U | 【填】 | 【填】 |

k 扫描原始数字（k = 5 / 10 / 20 / 50 / 100 / 200，单位：度）：

sphere
k=  5 mean_angle=2.9134°
k= 10 mean_angle=1.9810°
k= 20 mean_angle=1.6054°
k= 50 mean_angle=1.7836°
k=100 mean_angle=2.2686°
k=200 mean_angle=3.0372°
column
k=  5 mean_angle=1.5710°
k= 10 mean_angle=1.2670°
k= 20 mean_angle=1.2952°
k= 50 mean_angle=1.7309°
k=100 mean_angle=2.5296°
k=200 mean_angle=4.6137°
sphere_noisy
k=  5 mean_angle=2.9367°
k= 10 mean_angle=1.9816°
k= 20 mean_angle=1.6055°
k= 50 mean_angle=1.7789°
k=100 mean_angle=2.2716°
k=200 mean_angle=3.0410°
column_noisy
k=  5 mean_angle=13.8004°
k= 10 mean_angle=4.6335°
k= 20 mean_angle=2.3437°
k= 50 mean_angle=1.8874°
k=100 mean_angle=2.5699°
k=200 mean_angle=4.6572°

> 图：把「误差 vs k」画出来（matplotlib），存成 `error_vs_k.png`，放这里引用：`![误差曲线](error_vs_k.png)`

### 加噪右移（最优邻域的核心现象）

柱加 σ=0.01 噪声后：

- 最优 k 从 **10** 右移到 **50**
- k=5 误差从 **1.5** 升到 **13.8**（噪声主导小邻域）

球加噪几乎无变化，原因：r=100 尺度太大，σ=0.01 噪声忽略不计 → **噪声要匹配曲面局部尺度才有意义**。

### 真实数据（已砍，2026-09）

> 采样问题：`small_dutch.laz` 覆盖区域无植被点（class 3/4/5 缺失）、建筑点仅 73 个，真实数据验证**跳过**。合成曲面已完整验证「最优邻域」结论，真实数据留到有合适数据时再做。

### 三行结论

1. 平面无 U（曲率 0）
2. 柱深 U、球浅 U（U 的深浅 = 曲率）
3. 加噪后最优 k 右移（最优邻域随噪声移动）