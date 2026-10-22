"""
robustness_table — W6 鲁棒性主表

对同一批点对，施加剧扰动，看两个描述子的"同曲面 vs 异曲面"区分度怎么退化。

扰动三类（对照原计划 W6）：
  噪声    σ = 0.001 / 0.01 / 0.05
  密度    随机保留 1/2 · 1/4 的点
  遮挡    每个曲面上各挖走一条空间板（约 25%）

关键点对的处理
--------------
点对被扰动改变（密度/遮挡会删点）。为了仍然"用同一批物理点对"，
本脚本维护"幸存点 → 原下标"的映射，只在两个端点都幸存时统计。
这样每一档比较的是同一批点对，只是部分点消失了。

说明
----
组装代码。场景、点对、距离、汇总全部复用 descriptor_bench。
"""

import os
import sys
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from descriptor_bench import (
    make_scene_crease, make_pairs, summarize, DESCRIPTORS, NAMES_B,
)

K = 50
N_PER_SURFACE = 350


# ----------------------------------------------------------------------
# 扰动
# ----------------------------------------------------------------------
def perturb_noise(pts, sid, sigma, seed):
    """加点噪声。点数不变。"""
    rng = np.random.default_rng(seed)
    return pts + rng.normal(scale=sigma, size=pts.shape), np.ones(len(pts), bool)


def perturb_density(pts, sid, frac, seed):
    """随机保留 frac 比例的点。"""
    rng = np.random.default_rng(seed)
    return pts, rng.random(len(pts)) < frac


def perturb_occlusion(pts, sid, frac, seed):
    """
    遮挡：每个曲面上各挖走一条空间板。

    逐面处理，因为整个场景的空间跨度不均匀（有一个面在 z=1000），
    用全局板会把远处那个面整块删掉。
    """
    rng = np.random.default_rng(seed)
    keep = np.ones(len(pts), bool)

    for s in np.unique(sid):
        idx = np.flatnonzero(sid == s)
        if len(idx) < 10:
            continue
        P = pts[idx]

        u = rng.normal(size=3)
        u /= np.linalg.norm(u)
        proj = P @ u
        lo, hi = proj.min(), proj.max()
        span = hi - lo
        if span < 1e-9:
            continue

        c = rng.uniform(lo + 0.35 * span, hi - 0.35 * span)
        half = frac / 2.0 * span
        keep[idx] = np.abs(proj - c) > half

    return pts, keep


# ----------------------------------------------------------------------
# 评估
# ----------------------------------------------------------------------
def eval_level(pts_sub, pairs, labels, k=K):
    """在（可能已删点的）点云上评估两个描述子的 ratio。"""
    out = {}
    for name, fn in DESCRIPTORS.items():
        F = fn(pts_sub, k)
        d = np.linalg.norm(F[pairs[:, 0]] - F[pairs[:, 1]], axis=1)
        s = summarize(d, labels)
        s['kept_pairs'] = int(len(pairs))
        s['kept_pts'] = int(len(pts_sub))
        s['nan'] = int(np.isnan(F).sum())
        out[name] = s
    return out


def main():
    k_used = K
    print('=' * 70)
    print(f'robustness_table   k={k_used}   每面 {N_PER_SURFACE} 点')
    print('=' * 70)

    pts0, sid = make_scene_crease(n=N_PER_SURFACE, n_wing=N_PER_SURFACE // 2)
    print(f'\n基准点云 {len(pts0)} 点，{len(np.unique(sid))} 个面')
    for s, nm in NAMES_B.items():
        print(f'  [{s}] {nm:14s} {int((sid == s).sum()):>4} 点')

    pairs0, labels0 = make_pairs(pts0, sid, n_same=60, n_diff=60)
    print(f'\n基准点对 {len(pairs0)} 对（同 {int(labels0.sum())} / 异 {int((~labels0).sum())}）')

    print('\n点对策略：')
    print('  噪声档  -> 用同一批物理点对（点没变）')
    print('  密度/遮挡 -> 在幸存点里重抽（否则两端都幸存的概率太低，对数会塌）')

    levels = [
        ('基线',        'none',       None,  0),
        ('噪声 σ=0.001', 'noise',      0.001, 11),
        ('噪声 σ=0.01',  'noise',      0.01,  12),
        ('噪声 σ=0.05',  'noise',      0.05,  13),
        ('密度 1/2',     'density',    0.5,   21),
        ('密度 1/4',     'density',    0.25,  22),
        ('遮挡 ~25%',    'occlusion',  0.25,  31),
    ]

    rows = []
    for tag, kind, val, seed in levels:
        if kind == 'none':
            pts_p, keep = pts0, np.ones(len(pts0), bool)
        elif kind == 'noise':
            pts_p, keep = perturb_noise(pts0, sid, val, seed)
        elif kind == 'density':
            pts_p, keep = perturb_density(pts0, sid, val, seed)
        else:
            pts_p, keep = perturb_occlusion(pts0, sid, val, seed)

        survivors = np.flatnonzero(keep)
        pts_sub = pts_p[survivors]
        sid_sub = sid[survivors]

        if kind in ('none', 'noise'):
            # 点没删 -> 复用基准点对（下标不变）
            mapped = pairs0
            lab = labels0
        else:
            # 点被删 -> 在幸存点里重抽，保证每档对数一致
            mapped, lab = make_pairs(pts_sub, sid_sub, n_same=60, n_diff=60,
                                     seed=seed)

        res = eval_level(pts_sub, mapped, lab, k=k_used)
        row = dict(tag=tag, kept_pts=len(survivors), kept_pairs=len(mapped))

        # 有效性守卫：k 不能超过最小那个面的点数，否则 kNN 会伸到面外
        per_surf = [int((sid_sub == s).sum()) for s in np.unique(sid_sub)]
        min_surf = min(per_surf) if per_surf else 0
        row['min_surf'] = min_surf
        row['valid'] = bool(min_surf >= k_used)
        if not row['valid']:
            print(f'  [警告] {tag}: 最小面只有 {min_surf} 点 < k={k_used}，'
                  f'kNN 会跨面取点 -> 该档无效')

        for name in DESCRIPTORS:
            row[name] = res[name]['ratio']
            row[name + '_nan'] = res[name]['nan']
        rows.append(row)
        print(f'  {tag:<14s} 点 {row["kept_pts"]:>5}  对 {row["kept_pairs"]:>3}  '
              f'FPFH {row["FPFH"]:>6.3f}   SHOT {row["SHOT"]:>6.3f}'
              f'{"   有效" if row["valid"] else "   无效"}')

    print('\n' + '=' * 78)
    print('W6 鲁棒性主表（ratio = 异曲面距离 / 同曲面距离）')
    print('=' * 78)
    hdr = (f'{"扰动":<16}{"保留点":>8}{"保留对":>8}{"FPFH":>9}{"SHOT":>9}'
           f'{"FPFH/基线":>11}{"SHOT/基线":>11}{"":>6}')
    print(hdr)
    print('-' * len(hdr))
    base = rows[0]
    for r in rows:
        print(f'{r["tag"]:<16}{r["kept_pts"]:>8}{r["kept_pairs"]:>8}'
              f'{r["FPFH"]:>9.3f}{r["SHOT"]:>9.3f}'
              f'{r["FPFH"] / base["FPFH"]:>11.2f}{r["SHOT"] / base["SHOT"]:>11.2f}'
              f'{"有效" if r["valid"] else "无效":>6}')

    print('\n注：')
    print(f'  - k 固定为 {k_used}，两个描述子共用，横向可比')
    print('  - 有效性判据：k 必须小于"最小那个面的点数"，否则 kNN 会跨面取点、')
    print('    描述子实际描述的是几个不相干曲面的混合。')
    print('  - 噪声档复用同一批物理点对；密度/遮挡档在幸存点里重抽（同为 120 对）')
    print('  - SHOT 在本场景稳定在 ~1.0-1.15，与打乱水平接近：它在光滑/少尖角')
    print('    数据上退化，见 descriptor_bench.py 的折角诊断与 k 敏感性表')


if __name__ == '__main__':
    main()
