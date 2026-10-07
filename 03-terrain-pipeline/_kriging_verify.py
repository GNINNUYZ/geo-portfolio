# -*- coding: utf-8 -*-
"""kriging 验证探针 —— 不改动 kriging.py，用受控网格跑通并留下产物。

目的：
  1. 确认 pykrige 可用、kriging.py 的逻辑走得通
  2. 记录真实数据规模与耗时（供 M8 表② 当 HPC 对照基线）
  3. 留下输出产物（M0 #13 要求的"证据"）

保护措施：网格上限 MAX_CELLS，超了就整体放大步长；matplotlib 用 Agg（不弹窗）。
"""
import os
import sys
import time

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import laspy
from pykrige import OrdinaryKriging

sys.stdout.reconfigure(encoding='utf-8')

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, '..', 'data', 'C_37EN2.LAZ')
OUT = os.path.join(HERE, 'output')
os.makedirs(OUT, exist_ok=True)

CHUNK = 1_000_000
N_SAMPLE = 300
MAX_CELLS = 100_000        # 网格点数上限（保护内存与时间）

t0 = time.time()
with laspy.open(DATA) as reader:
    total = reader.header.point_count
    data0 = next(reader.chunk_iterator(CHUNK))
print('文件总点数      : %s' % format(total, ','))
print('读取第一个 chunk: %s 点   (%.1f s)' % (format(len(data0), ','), time.time() - t0))

ground = data0[data0.classification == 2]
print('其中 class 2 地面点: %s' % format(len(ground), ','))
if len(ground) < N_SAMPLE:
    sys.exit('地面点不足 %d 个，无法继续' % N_SAMPLE)

rng = np.random.default_rng(42)
idx = rng.choice(len(ground), N_SAMPLE, replace=False)
# laspy 的坐标字段是 ScaledArrayView（懒缩放视图），不是 numpy 数组：
#   .min()/.max() 可用，但 .mean()/.std() 等不支持 → 统一转成 numpy 数组再算
x = np.asarray(ground.x)[idx]
y = np.asarray(ground.y)[idx]
z = np.asarray(ground.z)[idx]
print('采样点数        : %d' % N_SAMPLE)
print('采样点范围      : X %.0f~%.0f  Y %.0f~%.0f' % (x.min(), x.max(), y.min(), y.max()))
print('采样点高程      : %.2f ~ %.2f m (均值 %.2f)' % (z.min(), z.max(), z.mean()))

# ---- 受控网格 ----
span_x, span_y = x.max() - x.min(), y.max() - y.min()
step = 2.0
nx, ny = int(span_x / step) + 1, int(span_y / step) + 1
if nx * ny > MAX_CELLS:
    scale = (nx * ny / MAX_CELLS) ** 0.5
    step = step * scale
    nx, ny = int(span_x / step) + 1, int(span_y / step) + 1
    print('网格超限，步长放大到 %.1f m' % step)

xs = np.arange(x.min(), x.max(), step)
ys = np.arange(y.min(), y.max(), step)
print('网格            : %d x %d = %s 格 (步长 %.1f m)' % (len(xs), len(ys), format(len(xs) * len(ys), ','), step))

# ---- kriging ----
t1 = time.time()
ok = OrdinaryKriging(x, y, z, variogram_model='spherical', verbose=False, enable_plotting=False)
print('拟合变差函数     : %.1f s' % (time.time() - t1))

t2 = time.time()
z_krig, sigma = ok.execute('grid', xs, ys)
dt = time.time() - t2
cells = len(xs) * len(ys)
print('kriging 执行     : %.1f s  (%s 格, %.2f ms/格)' % (dt, format(cells, ','), dt / cells * 1000))
print('预测高程        : %.2f ~ %.2f m' % (np.nanmin(z_krig), np.nanmax(z_krig)))
print('kriging 方差    : %.4f ~ %.4f' % (np.nanmin(sigma), np.nanmax(sigma)))

# ---- 产物 ----
f1 = os.path.join(OUT, 'kriging_surface.png')
f2 = os.path.join(OUT, 'kriging_variance.png')
fig, ax = plt.subplots(figsize=(8, 6))
im = ax.imshow(z_krig, cmap='terrain', origin='lower')
ax.set_title('Ordinary Kriging surface (spherical, %d pts, %.1f m grid)' % (N_SAMPLE, step))
fig.colorbar(im, ax=ax, label='Elevation (m)')
fig.tight_layout(); fig.savefig(f1, dpi=150); plt.close(fig)

fig, ax = plt.subplots(figsize=(8, 6))
im = ax.imshow(sigma, cmap='magma', origin='lower')
ax.set_title('Kriging variance')
fig.colorbar(im, ax=ax, label='Variance')
fig.tight_layout(); fig.savefig(f2, dpi=150); plt.close(fig)

print('已保存          : %s' % f1)
print('已保存          : %s' % f2)
print('总耗时          : %.1f s' % (time.time() - t0))
