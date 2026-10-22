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
| `pca_normal.py` | PCA normals + linearity/planarity/scattering + optimal-neighbourhood experiment |
| `orientation.py` | PCA normals + **MST global orientation** (Kruskal + union-find) |
| `fpfh.py` | **FPFH descriptor** (33-D, two-pass) |
| `SHOT.py` | **LRF + SHOT descriptor** (352-D) |
| `descriptor_bench.py` | **Descriptor comparison bench** (2 scenes + fold diagnostic + k-sensitivity) |
| `robustness_table.py` | **W6 robustness table** (noise / density / occlusion) |
| `diag_crease.py` | **cosθ validity diagnostic** (flat vs folded neighbourhood) |
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
| 球 | r=100 | 0.01 | 浅 U | 20 | 1.6 |
| 柱 | r=1 | 1 | 深 U | 50 | 1.8 |

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

---

## M2 法向全局定向（MST + 并查集）

`orientation.py` — PCA 法向的正负号是任意的（`n` 与 `−n` 同等合法），
必须用一条约定把它钉死，否则同一点在不同运行里得到相反法向。

### 方法

- **`compute_normals(points, k=20)`** — 逐点 PCA，最小特征值方向 = 法向。
- **`orient_mst(pts, normals, k_graph=10, seeds=None)`** — 在 kNN 图上建边，
  边权 = `1 − |n_i·n_j|`，用 **Kruskal 最小生成树 + 并查集** 建森林；
  再从种子点 BFS 传播：邻居法向与父节点同向则保留，否则取反。

为什么不用「视点法」（`n·(vp−p) > 0`）：视点法只对朝向观察者的面有效，
背面、遮挡处、闭合曲面内侧全部定错。MST 传播只依赖局部一致性，
不依赖视点，因此对闭合曲面和背面同样成立。

### 合成球面（1000 点，k=20，真值法向已知）

```
outter normal percentage: 100.00%
coherence:                100.00%
visible coherence ratio:  100.00%
DSU 连通分量: 1      MST 长度: 999
```

### 三行结论

1. 单点约定（视点法）在闭合曲面上必然错一部分
2. MST 传播把「局部一致」变成「全局一致」
3. 并查集避免 Kruskal 里的环，保证得到真正的森林

---

## M3a FPFH 描述子

`fpfh.py` — 手写 Fast Point Feature Histogram。

### 定义

**SPFH（单点）**：对点 `p` 的每个邻居 `q`，在 `p` 的局部坐标系里算三个角度并各分 11 箱：

```
u = n_p
v = (q − p) × u / ‖(q − p) × u‖
w = u × v
α = v · n_q
φ = u · (q − p) / ‖q − p‖
θ = arctan2(w · n_q, u · n_q)

α, φ ∈ [−1, 1]      θ ∈ [−π/3, π/3]
```

**FPFH（两点）**：

```
FPFH(p) = SPFH(p) + (1/k) · Σ_q (1/ω_q) · SPFH(q)        ω_q = ‖q − p‖
```

分两遍算：第一遍每个点算自己的 SPFH；第二遍按上式加权求和。输出 33 维（3 × 11）。

### 结果（场景 A：球/平/柱，各 1000 点，固定种子，50 同 / 50 异 点对）

```
ratio = mean(异曲面距离) / mean(同曲面距离)
打乱检验 = 把描述子行顺序随机打乱后重算，应回落到 ≈ 1（排除选题偏差）
```

| k | mean_same | mean_diff | **ratio** | 打乱均值 |
|---|---|---|---|---|
| 5 | 18.6344 | 24.3042 | 1.3043 | 0.941 |
| 10 | 11.7303 | 19.6929 | 1.6788 | 0.985 |
| **20** | **6.9953** | **15.7784** | **2.2556** | 0.990 |
| 40 | 4.2715 | 11.9911 | 2.8073 | 1.009 |

### 为什么 k=5 时 ratio 只有 1.30

`k=5` 的邻域半径约为球半径的 10%，**局部近似平面** —— 球面在这么小的窗口里
和平面在几何上确实分不开。`ratio ≈ 1` 是几何正确的，不是 bug。

**k 增大 = 邻域变大 = 曲率可见 = ratio 上升。** 这条对下文 SHOT 同样成立。

---

## M3b LRF + SHOT 描述子

`SHOT.py` — 手写 SHOT（Signature of Histograms of OrienTations）。

### LRF（局部参考系）

对每个点 `p` 和它的 k 近邻：

```
加权协方差   M = (1/Σw) · Σ w_i · (q_i − p)(q_i − p)ᵀ ,   w_i = r − d_i
特征分解     eigh(M) → λ0 ≤ λ1 ≤ λ2（升序）
z 轴 = 最小特征值方向（法向）      x 轴 = 次小特征值方向
y 轴 = z × x
```

**★ 符号消歧**：特征向量 `v` 和 `−v` 数学上等价，`eigh` 返回哪个是任意的。
约定：用邻域点投票，多数在负侧就翻转。`s == 0` 时必须保留原方向
（`np.sign(0) = 0` 会把轴乘成零向量）。

### LRF 验证

| 检验 | 结果 |
|---|---|
| 180° 旋转等变性 `‖LRF(R·P) − R·LRF(P)‖∞` | **6.106e-15** |
| 随机旋转 × 3 | 1.132e-14 / 8.438e-15 / 1.094e-14 |
| `det(R)` 全部 | **+1.000000**（右手系，无零轴） |
| 列模长偏离 1 | 8.88e-16 |
| 正交性 `‖RᵀR − I‖∞` | 2.00e-15 |
| 消歧不变式违反数 | **0** |

### SHOT（352 维）

```
352 = 32 分区 × 11 bin
 32 = 8 方位 × 2 俯仰 × 2 半径       （按邻居位置切块
 11 = cosθ 的直方图                  （按邻居法向计数

方位 = ⌊(atan2(v·y, v·x) + π) / (2π/8)⌋，钳到 0..7
俯仰 = (v·z ≥ 0)
半径 = (‖v‖ ≥ r/2)
分区 = 方位 + 8·俯仰 + 16·半径        （0..31，已验证是双射）

cosθ   = (邻居法向) · z               ∈ [−1, 1]
bin    = ⌊(cosθ + 1)/2 × 11⌋，钳到 0..10
扁平下标 = 分区 × 11 + bin            （0..351）
```

### SHOT 验证

| 检验 | 结果 |
|---|---|
| 形状 | `(150, 352)` |
| NaN / inf | 0 / 0 |
| 归一化后行和 | **精确 1.0**（全部行） |
| 零元素占比 | 0.965（19 邻居 vs 352 格，稀疏是固有的） |
| 被用到的列 | 227 / 352 |
| 32 分区是否全覆盖 | **32 / 32** |
| 计数守恒（归一化前） | 每点行和 = 邻居数 = k−1 = 19 |
| **任意旋转不变性** | **0.000e+00 × 3 次，100% 的行完全相同** |

### cosθ 有效性诊断（`diag_crease.py`）

造一个 90° 折角（两翼各 1.8 × 3.5，与球面等面积、等点距），
比较「邻域在平面内」与「邻域横跨折角」的 cosθ 分布：

| 位置 | 点数 | cosθ 范围 | 跨度 | 占用 bin |
|---|---|---|---|---|
| 远离折角（< 0.8） | 550 | `[+1.000, +1.000]` | **0.000** | **每点 1 个** |
| 折角附近（< 0.30） | 175 | `[−1.000, +1.000]` | **2.000** | **11 格全占**，每点中位 3、平均 3.20、最多 6 |

**结论**：平直区域 11 个 bin 只有 1 个非零，**直方图无信息**；
尖角区域铺满全部 11 个 bin。SHOT 的有效性依赖「邻域内存在尖角」。

---

## 描述子对比台（`descriptor_bench.py`）

在同一份点云、同一批点对上比较描述子。`ratio = 异曲面距离 / 同曲面距离`，
并附打乱检验作反假基线。

**两个场景**

- **A 光滑**：球 r=1 · 平 2×2 · 柱 r=0.5 h=4
- **B 含折角**：A + 90° 折角的两翼（各自独立成面）

**点对生成**：同曲面 50 对（轮流分配到各面）+ 异曲面 50 对
（**自动枚举所有面-面组合**，不再硬编码）。

### 场景级结果（k=20）

| 场景 | 描述子 | 维度 | mean_same | mean_diff | **ratio** | 打乱均值 | 判定 |
|---|---|---|---|---|---|---|---|
| A 光滑 | FPFH | 33 | 6.9953 | 15.7784 | **2.2556** | 0.990 | 区分度真实 |
| A 光滑 | SHOT | 352 | 0.3375 | 0.3831 | **1.1352** | 0.975 | 与噪声难分 |
| B 含折角 | FPFH | 33 | 4.9426 | 12.0219 | **2.4323** | 1.009 | 区分度真实 |
| B 含折角 | SHOT | 352 | 0.3292 | 0.3764 | **1.1432** | 0.985 | 与噪声难分 |

（FPFH 的每个 11-bin 子直方图内部已归一化成分布，但整个 33 维向量没有再归一化；
SHOT 做了整行 L1 归一化（行和 = 1）。两者绝对距离不可直接比；
`ratio` 是比值，对尺度不敏感，因此可比。）

### 一个被废弃的测法（保留作为教训）

最初按「翼 A × 翼 B」抽样测折角，结果 **FPFH ratio = 0.946、SHOT = 1.022**，
即完全无法区分。

**原因不是描述子坏了，是测法错了**：两翼各自都是平面，**旋转不变描述子对
「朝向不同但局部几何相同」的点必然给出几乎相同的描述子**。实测（都远离折角）：

| 描述子 | 同翼 | 跨翼 | 跨/同 |
|---|---|---|---|
| FPFH | 3.9303 | 3.5150 | 0.894 |
| SHOT | 0.3074 | 0.2955 | 0.961 |

**教训**：测「不同曲面」必须制造「邻域内几何不同」，而不是「整体朝向不同」。
修正后的测法见下。

### 折角敏感性（正确测法：平邻域 vs 含折角邻域）

| 描述子 | k | 非零占比 | 同几何 | 异几何 | **ratio** |
|---|---|---|---|---|---|
| FPFH | 20 | 0.188 | 6.1501 | 11.4023 | 1.854 |
| FPFH | 50 | 0.262 | 2.7227 | 9.1549 | 3.362 |
| FPFH | 100 | 0.338 | 1.5087 | 7.9364 | 5.260 |
| FPFH | 200 | 0.449 | 0.9318 | 6.2695 | **6.728** |
| SHOT | 20 | 0.029 | 0.2934 | 0.3414 | 1.164 |
| SHOT | 50 | 0.042 | 0.2075 | 0.3095 | 1.491 |
| SHOT | 100 | 0.049 | 0.1757 | 0.3178 | 1.809 |
| SHOT | 200 | 0.055 | 0.1724 | 0.3291 | **1.909** |

**SHOT 欠参数**：`k=20` 时只有 19 个邻居去填 352 个格子（非零占比 2.9%）。
`k=200` 时非零占比仍仅 5.5% —— 因为平邻域里所有邻居的 cosθ 都等于 1，
挤进同一个 bin，**每个分区只有 1 格有数**。这是结构性稀疏，不是邻居不够。

---

## W6 鲁棒性主表（`robustness_table.py`）

场景 B（5 个面），`k=50`，每档 120 对（60 同 / 60 异）。

| 扰动 | 保留点 | FPFH | SHOT | FPFH/基线 | SHOT/基线 | 有效 |
|---|---|---|---|---|---|---|
| **基线** | 1400 | **2.871** | 1.145 | 1.00 | 1.00 | 有效 |
| 噪声 σ=0.001 | 1400 | 2.849 | 1.036 | 0.99 | 0.91 | 有效 |
| 噪声 σ=0.01 | 1400 | 2.689 | 1.044 | 0.94 | 0.91 | 有效 |
| **噪声 σ=0.05** | 1400 | **2.240** | 1.019 | **0.78** | 0.89 | 有效 |
| **密度 1/2** | 690 | **2.245** | 1.111 | **0.78** | 0.97 | 有效 |
| 密度 1/4 | 361 | 2.974 | 1.133 | 1.04 | 0.99 | **无效** |
| **遮挡 ~25%** | 991 | **2.069** | 1.076 | **0.72** | 0.94 | 有效 |

**点对策略**：噪声档复用同一批物理点对（点没变）；密度/遮挡档在幸存点里重抽
（否则两端都幸存的概率是 `f²`，密度 1/4 时 60 对只剩 4 对，统计无意义）。

**有效性判据**：`k` 必须小于「最小那个面的点数」，否则 kNN 会伸到面外，
描述子实际描述的是几个不相干曲面的混合。

> **密度 1/4 档被判无效**：折角翼只剩 43 点 < k=50。
> 这一档的 `1.04`（看起来最好）恰恰是最不可信的数。

### 三条结论

1. **FPFH 最怕遮挡**（0.72×），其次是 σ=0.05 噪声和密度减半（都 0.78×）。
2. **SHOT 那列看着稳定（0.89–0.99），但是假稳定** —— 它的基线 1.145 本身
   就在打乱水平（0.975）附近，已经在最低水平，没有退化空间。
3. **无效档必须标出来**，否则会得出相反的结论。

---

## 复现

```bash
# 环境
python -m venv .venv && .venv/Scripts/pip install numpy scipy laspy lazrs

# 定向
python orientation.py

# 描述子对比台（两场景 + 折角诊断 + k 敏感性，约 180 s）
python descriptor_bench.py

# W6 鲁棒性主表（约 65 s）
python robustness_table.py

# cosθ 有效性诊断（约 30 s）
python diag_crease.py
```

所有脚本都用固定随机种子，结果可复现。

---

## 已知限制

| # | 限制 | 影响 |
|---|---|---|
| 1 | SHOT 的 11-bin 直方图在光滑面上退化（11 格只用 1 格） | 合成光滑曲面低估 SHOT；真实建筑点云（尖角多）应更好 |
| 2 | SHOT 需要远大于 20 的邻域才不稀疏（k=200 时非零占比仍仅 5.5%） | 与 FPFH 横向比较必须声明 k，或用半径邻域 |
| 3 | 本 bench 的「不同曲面」是几何基本形（球/平/柱/折角） | 未覆盖真实扫描的噪声结构、遮挡形态、非均匀密度 |
| 4 | 密度 1/4 档无效（最小面点数 < k） | 该档数字不可用 |
| 5 | 真实数据（`small_dutch.laz`）未接入本 bench | 建筑点云覆盖区域无植被点、建筑点仅 73 个，见 M1 说明 |
| 6 | 运行时间为纯 Python 串行 | 20000 点 FPFH 约 52 s；加速属并行层（L5）工作 |
