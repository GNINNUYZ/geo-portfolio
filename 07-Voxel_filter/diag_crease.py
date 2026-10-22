"""
诊断：折角附近的 cosθ 是否散开？

问题
----
SHOT 的 352 维 = 32 分区 x 11 bin(cosθ 直方图)。
但在光滑曲面上实测 cosθ 跨度只有 0.19（约 1 个 bin），
11 个 bin 的信息量几乎为零。

本脚本造一个 90° 折角，比较：
    折角附近（邻域横跨两翼）  vs  远离折角（邻域在单一平面内）
的 cosθ 分布。

若"折角附近"的 cosθ 明显散开 -> SHOT 的直方图在真实数据（尖角多）上有信息。
若两者都不散 -> 实现或参数有问题。

只做诊断，不进入 bench 的主指标。
"""

import sys
import os
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import kdtree
import orientation as ori
from SHOT import lrf

BIN_WIDTH = 2.0 / 11.0


def make_crease(n_per_wing=500,
                wing=1.8, depth=3.5,
                z_offset=0.0, seed=0):
    """
    造一个 90 度折角（翻开的书）。

    水平翼: z = z_offset,  x in [0, wing],      y in [-depth/2, depth/2]
    竖直翼: x = 0,         z in [z_offset, z_offset+wing], y in [-depth/2, depth/2]

    折角线: x = 0, z = z_offset, 沿 y 方向。

    返回
    ----
    pts       (N,3)
    wing_id   (N,)   0 = 水平翼, 1 = 竖直翼
    d_crease  (N,)   到折角线的距离 = sqrt(x^2 + (z-z_offset)^2)
    """
    rng = np.random.default_rng(seed)

    y = rng.uniform(-depth / 2, depth / 2, n_per_wing)

    # 水平翼
    x_h = rng.uniform(0, wing, n_per_wing)
    z_h = np.full(n_per_wing, z_offset)
    wing_h = np.column_stack([x_h, y, z_h])

    # 竖直翼
    x_v = np.zeros(n_per_wing)
    z_v = rng.uniform(z_offset, z_offset + wing, n_per_wing)
    wing_v = np.column_stack([x_v, y, z_v])

    pts = np.vstack([wing_h, wing_v])
    wing_id = np.concatenate([np.zeros(n_per_wing, int),
                              np.ones(n_per_wing, int)])
    d_crease = np.sqrt(pts[:, 0] ** 2 + (pts[:, 2] - z_offset) ** 2)

    return pts, wing_id, d_crease


def cos_theta_per_point(pts, k=20):
    """
    复算 SHOT 的 cosθ：对每个点，取它邻域内每个邻居的法向与 LRF z 轴的夹角余弦。

    返回
    ----
    list of 1-D arrays，每个点一个（长度 = 邻居数）
    """
    L = lrf(pts, k)
    nrm, _ = ori.compute_normals(pts, 20)
    nrm = ori.orient_mst(pts, nrm)
    tree = kdtree.build(pts)
    N = len(pts)

    out = []
    for i in range(N):
        nb = [j for j in kdtree.kNN(tree, pts, pts[i], k) if j != i]
        if len(nb) < 3:
            out.append(np.array([]))
            continue
        z = L[i][:, 2]
        out.append(nrm[nb] @ z)
    return out


def report(cos_list, mask, tag):
    """统计被 mask 选中的那些点的 cosθ 汇总。"""
    vals = [c for c, m in zip(cos_list, mask) if m and len(c) > 0]
    if not vals:
        print(f'  {tag}: 无有效点')
        return None
    c = np.concatenate(vals)

    # 每个点占用了几个 bin
    bins_per_point = []
    for v in vals:
        b = np.clip(np.floor((v + 1) / 2 * 11).astype(int), 0, 10)
        bins_per_point.append(len(np.unique(b)))

    lo, hi = c.min(), c.max()
    spread = hi - lo

    print(f'  {tag}')
    print(f'    点数           = {len(vals)}')
    print(f'    cosθ 范围      = [{lo:+.3f}, {hi:+.3f}]   跨度 {spread:.3f}')
    print(f'    标准差         = {c.std():.4f}')
    print(f'    跨度 / bin宽   = {spread / BIN_WIDTH:.2f} 个 bin')
    print(f'    每点占用 bin 数 = 中位 {np.median(bins_per_point):.0f}, '
          f'平均 {np.mean(bins_per_point):.2f}, 最大 {max(bins_per_point)}')
    return dict(spread=spread, std=c.std(), bins=np.mean(bins_per_point))


def main():
    print('=' * 62)
    print('诊断：折角附近的 cosθ 是否散开')
    print('=' * 62)
    print(f'11 个 bin 覆盖 [-1,1]，每格宽 {BIN_WIDTH:.4f}')
    print(f'要跨 1 格，法向需偏约 35 度；跨 2 格约 45 度\n')

    pts, wing_id, d_crease = make_crease()
    print(f'折角点云：{len(pts)} 点（两翼各 500）')
    print(f'  面积 = 2 x 1.8 x 3.5 = {2 * 1.8 * 3.5:.2f}（球面是 12.57）')
    print(f'  平均点间距约 0.11（与球/平/柱一致）')
    print(f'  两翼法向夹角 = 90 度')
    print()

    cos_list = cos_theta_per_point(pts, k=20)

    near = d_crease < 0.30        # 邻域半径约 0.25-0.3，会横跨两翼
    far = d_crease > 0.80         # 邻域完全在单一平面内

    print('-' * 62)
    report(cos_list, far,  '【A】远离折角（邻域只在一个平面内）')
    print()
    report(cos_list, near, '【B】折角附近（邻域横跨两翼）')
    print('-' * 62)
    print()

    print('结论：')
    v_far = [c for c, m in zip(cos_list, far) if m and len(c) > 0]
    v_near = [c for c, m in zip(cos_list, near) if m and len(c) > 0]
    if v_far and v_near:
        sp_far = np.concatenate(v_far)
        sp_near = np.concatenate(v_near)
        range_far = sp_far.max() - sp_far.min()
        range_near = sp_near.max() - sp_near.min()
        if range_far < 1e-9:
            print(f'  平面内的 cosθ 跨度 = 0（所有值都是 {sp_far.min():+.3f}）')
            print(f'  折角处的 cosθ 跨度 = {range_near:.3f}'
                  f'（占满 {range_near / BIN_WIDTH:.1f} 个 bin）')
            print('  -> 平面内：11 个 bin 里只有 1 个非零，直方图无信息')
            print('  -> 折角处：直方图铺满，信息量充分')
            print('  -> 结论：SHOT 的 11 bin 在含尖角的真实数据上是有信息的。')
        else:
            ratio = range_near / range_far
            print(f'  折角处 cosθ 跨度 / 平面内跨度 = {ratio:.2f}x')
            if ratio > 3:
                print('  -> 折角处显著散开。SHOT 的 11 bin 在含尖角的真实数据上是有信息的。')
            elif ratio > 1.5:
                print('  -> 折角处散开一些，但幅度有限。')
            else:
                print('  -> 两者接近，说明 cosθ 直方图在这里也没起作用，需检查实现或参数。')


if __name__ == '__main__':
    main()
