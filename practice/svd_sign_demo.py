# -*- coding: utf-8 -*-
"""Why Vt.T @ U gives an unpredictable sign: it is not a rotation matrix at all."""
import numpy as np

np.random.seed(0)


def report(label, M):
    print('%-22s det = %+ .6f   orthonormal? %s   ||M.T@M - I|| = %.3e'
          % (label, np.linalg.det(M),
             np.allclose(M.T @ M, np.eye(3), atol=1e-8),
             np.linalg.norm(M.T @ M - np.eye(3))))


print('=== 1) 完全按你的写法（h = A @ B，B 未中心化）===')
for trial in range(6):
    A = np.eye(3)
    B = np.random.rand(3, 3)
    B = B - B.mean()
    h = A @ B
    U, E, Vt = np.linalg.svd(h)
    dR_wrong = Vt.T @ U          # 你写的
    dR_right = Vt.T @ U.T        # 正确（= V @ U^T）
    print('trial %d:  det(V.T@U) = %+ .6f    det(V.T@U.T) = %+ .6f'
          % (trial, np.linalg.det(dR_wrong), np.linalg.det(dR_right)))

print()
print('=== 2) 关键：V.T @ U 不是正交矩阵 ===')
A = np.eye(3)
B = np.random.rand(3, 3) - 0.5
U, E, Vt = np.linalg.svd(A @ B)
report('V.T @ U   (你写的)', Vt.T @ U)
report('V.T @ U.T (正确的)', Vt.T @ U.T)
print()
print('SVD 保证的是 U 和 V 各自正交（U.T@U = I, Vt@Vt.T = I），')
print('但 V.T @ U 是两个"不同"正交矩阵的乘积，当 V != U 时它不是正交的。')
print('行列式的绝对值也就不是 1 —— 所以它随数据随机变化。')

print()
print('=== 3) 用真正的 Kabsch（中心化 + 互协方差）===')
for trial in range(4):
    X = np.random.randn(200, 3)
    ang = 0.7
    Rt = np.array([[np.cos(ang), -np.sin(ang), 0],
                   [np.sin(ang), np.cos(ang), 0], [0, 0, 1]])
    Y = X @ Rt.T + np.array([1.0, 2.0, 3.0])
    Xc = X - X.mean(0)
    Yc = Y - Y.mean(0)
    H = Xc.T @ Yc
    U, E, Vt = np.linalg.svd(H)
    dR = Vt.T @ U.T
    print('trial %d:  S = %s   det = %+ .6f   ||dR - Rt|| = %.2e'
          % (trial, np.round(E, 4), np.linalg.det(dR), np.linalg.norm(dR - Rt)))

print()
print('=== 4) 平面点云：奇异值掉到 0，符号就不可靠 ===')
ang = 0.7
Rt = np.array([[np.cos(ang), -np.sin(ang), 0],
               [np.sin(ang), np.cos(ang), 0], [0, 0, 1]])
for label, pts in [
    ('一般立体点云', np.random.randn(300, 3)),
    ('完全共面 z=0', np.column_stack([np.random.randn(300, 2), np.zeros(300)])),
    ('近共面 z~1e-9', np.column_stack([np.random.randn(300, 2), np.random.randn(300) * 1e-9])),
]:
    Y = pts @ Rt.T
    Xc = pts - pts.mean(0)
    Yc = Y - Y.mean(0)
    U, E, Vt = np.linalg.svd(Xc.T @ Yc)
    dR = Vt.T @ U.T
    if np.linalg.det(dR) < 0:
        Vt2 = Vt.copy()
        Vt2[2, :] *= -1
        dR = Vt2.T @ U.T
    print('%-14s S = %s  -> det = %+ .6f  误差 = %.2e'
          % (label, np.round(E, 8), np.linalg.det(dR), np.linalg.norm(dR - Rt)))

print()
print('=== 5) 符号歧义的来源：翻转同一对奇异向量，H 不变 ===')
X = np.random.randn(300, 3)
Xc = X - X.mean(0)
H = Xc.T @ Xc
U, E, Vt = np.linalg.svd(H)
U2, Vt2 = U.copy(), Vt.copy()
U2[:, 2] *= -1
Vt2[2, :] *= -1
print('||H - H_flipped|| = %.3e   -> 两个 SVD 都合法，但给出的 R 符号可能相反'
      % np.linalg.norm(U @ np.diag(E) @ Vt - U2 @ np.diag(E) @ Vt2))
print('det(U S Vt)   = %+.4f' % np.linalg.det(Vt.T @ U.T))
print('det(U2 S Vt2) = %+.4f' % np.linalg.det(Vt2.T @ U2.T))
