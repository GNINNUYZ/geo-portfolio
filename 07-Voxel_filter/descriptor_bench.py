"""
descriptor_bench — 描述子对比台

用途
----
在同一份点云、同一批点对上，比较不同描述子的"同曲面 vs 异曲面"区分度。

  ratio = mean(异曲面描述子距离) / mean(同曲面描述子距离)

ratio > 1 = 有区分度。所有结果都附"打乱检验"（把描述子行顺序随机打乱后
ratio 应回落到 ~1），用来排除"ratio 高是因为选题偏差"。

两个场景
--------
场景 A（光滑）：球 r=1 · 平 2x2 · 柱 r=0.5 h=4
场景 B（含折角）：A + 90° 折角的两翼（翼A / 翼B，各自独立成面）

第二个场景是为了回答一个问题：
    SHOT 的 11-bin 直方图在光滑曲面上退化（见 diag_crease.py），
    那在含尖角的场景里，它的 ratio 会不会升上去？

说明
----
本文件是组装代码。make_pairs / pair_dis / summarize 的初版来自早期草稿，
本版把 combos 的硬编码改成自动枚举，使面数增加时无需改代码。
"""

import os
import sys
import itertools
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import fpfh
from SHOT import shot


# ----------------------------------------------------------------------
# 场景 A：三个光滑曲面
# ----------------------------------------------------------------------
NAMES_A = {0: '球 r=1', 1: '平 2x2', 2: '柱 r=0.5 h=4'}


def make_scene_smooth(n=1000, seed=0):
    """球 / 平 / 柱，面积与点间距已对齐。"""
    rng = np.random.default_rng(seed)

    r = 1.0
    theta = np.arccos(rng.uniform(-1, 1, n))
    phi = rng.uniform(0, 2 * np.pi, n)
    sphere = np.column_stack([
        r * np.sin(theta) * np.cos(phi),
        r * np.sin(theta) * np.sin(phi),
        r * np.cos(theta),
    ])

    plane = np.column_stack([
        rng.uniform(-1, 1, n),
        rng.uniform(-1, 1, n),
        np.full(n, 1000.0),
    ])

    r = 0.5
    ang = rng.uniform(0, 2 * np.pi, n)
    cylinder = np.column_stack([
        r * np.cos(ang),
        r * np.sin(ang),
        rng.uniform(3, 7, n),
    ])

    pts = np.vstack([sphere, plane, cylinder])
    sid = np.concatenate([np.full(n, 0, int),
                          np.full(n, 1, int),
                          np.full(n, 2, int)])
    return pts, sid


# ----------------------------------------------------------------------
# 场景 B：场景 A + 90 度折角
# ----------------------------------------------------------------------
NAMES_B = dict(NAMES_A)
NAMES_B.update({3: '折角-水平翼', 4: '折角-垂直翼'})

CREASE_Z = 10.0
WING = 1.8
DEPTH = 3.5


def make_crease_wings(n=500, seed=1):
    """
    90 度折角：两块 1.8 x 3.5 的平板沿一条线折起来。

      水平翼: z = 10,   x in [0, 1.8],      y in [-1.75, 1.75]
      竖直翼: x = 0,    z in [10, 11.8],    y in [-1.75, 1.75]

    折角线: x=0, z=10, 沿 y 方向。两翼法向夹角 = 90 度。
    每翼面积 6.3，合计 12.6（与球面 12.57 对齐 -> 点间距一致）。
    """
    rng = np.random.default_rng(seed)
    y = rng.uniform(-DEPTH / 2, DEPTH / 2, n)

    wing_h = np.column_stack([rng.uniform(0, WING, n), y,
                              np.full(n, CREASE_Z)])
    wing_v = np.column_stack([np.zeros(n), y,
                              rng.uniform(CREASE_Z, CREASE_Z + WING, n)])
    return wing_h, wing_v


def make_scene_crease(n=1000, n_wing=500, seed=0):
    """场景 A + 折角两翼（翼A=3, 翼B=4，各自独立成面）。"""
    pts_a, sid_a = make_scene_smooth(n=n, seed=seed)
    wing_h, wing_v = make_crease_wings(n=n_wing, seed=seed + 1)
    pts = np.vstack([pts_a, wing_h, wing_v])
    sid = np.concatenate([sid_a,
                          np.full(len(wing_h), 3, int),
                          np.full(len(wing_v), 4, int)])
    return pts, sid


# ----------------------------------------------------------------------
# 点对
# ----------------------------------------------------------------------
def make_pairs(pts, surface_id, n_same=50, n_diff=50, seed=42):
    """
    出题：同曲面 / 异曲面的点对下标。

    同曲面对：随机挑一个面，在该面内取 2 个不同点（轮流分配）
    异曲面对：自动枚举所有"面-面"组合，轮流分配
    """
    rng = np.random.default_rng(seed)
    ids = np.unique(surface_id)
    groups = {k: np.flatnonzero(surface_id == k) for k in ids}

    same_pairs = []
    for t in range(n_same):
        k = ids[t % len(ids)]
        a, b = rng.choice(groups[k], 2, replace=False)
        same_pairs.append((a, b))

    combos = list(itertools.combinations(ids, 2))     # 随面数自动扩展
    diff_pairs = []
    for t in range(n_diff):
        k1, k2 = combos[t % len(combos)]
        a = rng.choice(groups[k1])
        b = rng.choice(groups[k2])
        diff_pairs.append((a, b))

    pairs = np.array(same_pairs + diff_pairs, dtype=np.int64)
    labels = np.array([True] * len(same_pairs) + [False] * len(diff_pairs))
    return pairs, labels


def pair_dis(F, pairs):
    """每对的描述子欧氏距离。F:(N,D), pairs:(P,2) -> (P,)"""
    return np.linalg.norm(F[pairs[:, 0]] - F[pairs[:, 1]], axis=1)


def summarize(d, labels):
    d_same, d_diff = d[labels], d[~labels]
    return {
        'mean_same': float(d_same.mean()),
        'median_same': float(np.median(d_same)),
        'mean_diff': float(d_diff.mean()),
        'median_diff': float(np.median(d_diff)),
        'ratio': float(d_diff.mean() / d_same.mean()),
        'n_same': int(len(d_same)),
        'n_diff': int(len(d_diff)),
    }


def check_pairs(surface_id, pairs, labels):
    a, b = pairs[:, 0], pairs[:, 1]
    return {
        'no_self_pair': bool((a != b).all()),
        'same_truly_same': bool((surface_id[a[labels]] == surface_id[b[labels]]).all()),
        'diff_truly_diff': bool((surface_id[a[~labels]] != surface_id[b[~labels]]).all()),
    }


def fold_pairs(surface_id, wing_a, wing_b, n_same=100, n_diff=100, seed=7):
    """
    【已废弃】按翼 id 抽样测折角。

    为什么废弃：两翼都是平面，旋转不变描述子（FPFH/SHOT）对"朝向不同但
    局部几何相同"的点给出几乎相同的描述子。实测跨翼/同翼 ≈ 0.89~0.96，
    接近 1 —— 是这个测试设计错了，不是描述子错了。
    正确做法见 flat_vs_fold()。
    """
    rng = np.random.default_rng(seed)
    ga = np.flatnonzero(surface_id == wing_a)
    gb = np.flatnonzero(surface_id == wing_b)
    sp = []
    for t in range(n_same):
        g = ga if t % 2 == 0 else gb
        a, b = rng.choice(g, 2, replace=False)
        sp.append((a, b))
    dp = [(rng.choice(ga), rng.choice(gb)) for _ in range(n_diff)]
    return (np.array(sp + dp, dtype=np.int64),
            np.array([True] * len(sp) + [False] * len(dp)))


def flat_vs_fold(F, d_crease, near_th=0.30, far_th=0.80,
                 n=400, seed=0):
    """
    正确的折角测试：比较"平的邻域" 与 "含折角的邻域"。

      同几何对 = 两个都远离折角的点（邻域都在单一平面内）
      异几何对 = 一个远离折角的点 + 一个折角附近的点（邻域横跨两翼）

    这才是真正的"局部几何不同"，而不是"朝向不同"。
    """
    rng = np.random.default_rng(seed)
    near = np.flatnonzero(d_crease < near_th)
    far = np.flatnonzero(d_crease > far_th)
    if len(near) < 2 or len(far) < 2:
        return None

    same, diff = [], []
    for _ in range(n):
        a, b = rng.choice(far, 2, replace=False)
        same.append(np.linalg.norm(F[a] - F[b]))
        c = rng.choice(near)
        diff.append(np.linalg.norm(F[a] - F[c]))
    same, diff = np.array(same), np.array(diff)
    return {
        'mean_same': float(same.mean()),
        'mean_diff': float(diff.mean()),
        'ratio': float(diff.mean() / same.mean()),
        'n_near': int(len(near)),
        'n_far': int(len(far)),
    }


# ----------------------------------------------------------------------
# 描述子
# ----------------------------------------------------------------------
DESCRIPTORS = {
    'FPFH': lambda pts, k: fpfh.compute_fpfh(pts, k),
    'SHOT': lambda pts, k: shot(pts, k),
}


def run_one(name, fn, pts, pairs, labels, k, n_shuffle=5):
    F = fn(pts, k)
    d = pair_dis(F, pairs)
    s = summarize(d, labels)

    rng = np.random.default_rng(0)
    rs = np.array([summarize(pair_dis(F[rng.permutation(len(F))], pairs),
                             labels)['ratio'] for _ in range(n_shuffle)])
    s.update(dict(name=name, dim=F.shape[1], nan=int(np.isnan(F).sum()),
                  shuffle_mean=float(rs.mean()),
                  shuffle_lo=float(rs.min()), shuffle_hi=float(rs.max())))
    s['ok'] = s['ratio'] > s['shuffle_hi'] * 1.15
    return s, F


def print_block(tag, pts, sid, names, k, n_same=50, n_diff=50):
    print('\n' + '=' * 68)
    print(f'场景 {tag}   k={k}   点数={len(pts)}   面数={len(np.unique(sid))}')
    print('=' * 68)
    for s_, nm in names.items():
        P = pts[sid == s_]
        print(f'  [{s_}] {nm:14s} {len(P):>5} 点  '
              f'包围盒 {np.round(P.min(0), 2)} ~ {np.round(P.max(0), 2)}')

    pairs, labels = make_pairs(pts, sid, n_same, n_diff)
    chk = check_pairs(sid, pairs, labels)
    print(f'\n  出题自检 {chk}')
    assert all(chk.values()), 'make_pairs 出题有问题'
    print(f'  共 {len(pairs)} 对（同 {labels.sum()} / 异 {(~labels).sum()}）')

    out = {}
    for name, fn in DESCRIPTORS.items():
        s, F = run_one(name, fn, pts, pairs, labels, k)
        out[name] = s
        print(f'\n  --- {name} (dim={s["dim"]}, NaN={s["nan"]}) ---')
        print(f'    同曲面 mean={s["mean_same"]:.4f}  异曲面 mean={s["mean_diff"]:.4f}')
        print(f'    ratio = {s["ratio"]:.4f}')
        print(f'    打乱  mean={s["shuffle_mean"]:.3f}  '
              f'范围[{s["shuffle_lo"]:.3f}, {s["shuffle_hi"]:.3f}]')
        print(f'    判定  {"区分度真实" if s["ok"] else "与噪声难分"}')
    return out


def print_fold_block(k=20, n_wing=1500):
    """
    折角诊断：平邻域 vs 含折角邻域。

    这是"局部几何不同"的正确测法。同时给 k 敏感性 —— 因为 SHOT 的 352 维
    需要足够的邻居数才不稀疏。
    """
    print('\n' + '=' * 68)
    print('折角诊断：平的邻域  vs  含 90° 折角的邻域')
    print('=' * 68)

    wh, wv = make_crease_wings(n=n_wing, seed=1)
    pts = np.vstack([wh, wv])
    d = np.sqrt(pts[:, 0] ** 2 + (pts[:, 2] - CREASE_Z) ** 2)
    print(f'  点云 {len(pts)} 点（两翼各 {n_wing}）')
    print(f'  折角附近(<0.30) {int((d < 0.30).sum())} 点 · '
          f'远离(>0.80) {int((d > 0.80).sum())} 点')

    rows = []
    for name, fn in DESCRIPTORS.items():
        for kk in (20, 50, 100, 200):
            F = fn(pts, kk)
            r = flat_vs_fold(F, d)
            if r is None:
                continue
            rows.append((name, kk, (F != 0).mean(), r))

    print(f'\n  {"描述子":<7}{"k":>5}{"非零占比":>10}{"同几何":>10}'
          f'{"异几何":>10}{"ratio":>9}')
    print('  ' + '-' * 51)
    for name, kk, nz, r in rows:
        print(f'  {name:<7}{kk:>5}{nz:>10.3f}{r["mean_same"]:>10.4f}'
              f'{r["mean_diff"]:>10.4f}{r["ratio"]:>9.3f}')

    print('\n  读法：')
    print('    SHOT 的 k 越大 ratio 越高 —— 因为 352 维需要足够多的邻居才不稀疏。')
    print('    k=20 时只有 19 个邻居填 352 个格子（非零占比 3%），信息表达不出来。')


def main():
    k = 20
    res = {}

    pts_a, sid_a = make_scene_smooth()
    res['A 光滑'] = print_block('A · 光滑三面', pts_a, sid_a, NAMES_A, k)

    pts_b, sid_b = make_scene_crease()
    res['B 含折角'] = print_block('B · 光滑 + 90° 折角', pts_b, sid_b, NAMES_B, k)

    print('\n' + '=' * 68)
    print('汇总（场景级 ratio）')
    print('=' * 68)
    hdr = (f'{"场景":<12}{"描述子":<8}{"维度":>6}{"ratio":>9}'
           f'{"打乱均值":>10}{"判定":>14}')
    print(hdr)
    print('-' * len(hdr))
    for scene, d in res.items():
        for name, s in d.items():
            print(f'{scene:<12}{name:<8}{s["dim"]:>6}{s["ratio"]:>9.4f}'
                  f'{s["shuffle_mean"]:>10.3f}'
                  f'{"区分度真实" if s["ok"] else "与噪声难分":>14}')

    print_fold_block()


if __name__ == '__main__':
    main()
