# ML — PointNet 复现（ModelNet40 分类）

从论文实现 PointNet（[Qi et al., 2017](https://arxiv.org/abs/1612.00593)），在 ModelNet40 上做 40 类形状分类。
本 README 按仓库约定补齐：**背景 / 数据 / 方法 / 结果（数字）/ 如何运行**。

## 结果

| 指标 | 值 |
|---|---|
| ModelNet40 test accuracy | **86%** |
| 训练轮数 | **200 epoch，无提前停止**（见训练曲线） |
| 10 epoch 时 | ~81.7%（中间结果，**不再引用**） |
| 训练设备 | NVIDIA RTX 5060 Ti 16 GB（`.venv` 内 torch 2.12.1+cu130，`cuda.is_available() == True`） |

**训练曲线**：`figure_training_curve.png` —— 横轴 0→200 epoch，约 50 epoch 后进入平台并稳定在 **0.86–0.87**。这是 86% 的直接证据。
> 口径已统一：**86%**（CV 与动机信一致）；81.7% 是 10 epoch 的中间结果，作废。
> ⚠️ 仍未记录：总训练耗时（`pointnet.py` 只打印到 stdout，没有落盘日志）。

## 数据

- **ModelNet40**（`data/modelnet40/ModelNet40`），40 个类别，训练/测试划分按原数据集的 `train` / `test` 子目录
- 每个网格采样 **1,024 点**，两种关键处理（`provider.py`）：
  - **面积加权采样**：按三角形面积归一化为概率 `p = areas / areas.sum()`，再在三角形内用重心坐标采样（`s = √u`，保证面内均匀）
  - **单位球归一化**：先去均值，再除以最大点范数（`pc / max‖pc‖`）→ 所有形状落在单位球内
- `DataLoader`：batch size 128，训练集 shuffle

## 方法（`pointnet.py`）

- **T-Net ×2**：输入变换（k=3）与特征变换（k=64），都是 `Conv1d → BN → ReLU` 堆叠 + `amax` 池化 + FC，输出残差加到单位矩阵上（`x + I`）
- **共享 MLP**：`3→64→64`（逐点），特征变换后接 `64→128→256→1024`（逐点，1×1 卷积）
- **对称函数**：`amax(dim=2)` 全局最大池化 → 置换不变
- **分类头**：`1024→512→256→40`，含 BatchNorm + ReLU + **Dropout 0.3**
- **损失**：`CrossEntropyLoss + 0.001 × ortho_loss(A)`，其中 `ortho_loss(A) = MSE(A Aᵀ, I)`
  —— 这是论文里的**特征变换正交正则项**，用来让 64×64 变换矩阵接近正交
- **优化**：Adam（lr = 1e-3）+ `StepLR(step_size=20, gamma=0.5)`
- **训练**：最多 200 epoch；每 epoch 在测试集上算一次准确率并打印

## 文件

| 文件 | 说明 |
|---|---|
| `pointnet.py` | 模型定义 + 训练循环（含正交正则、测试集评估、曲线保存） |
| `provider.py` | ModelNet40 读取（OFF 解析）、面积加权采样、单位球归一化、DataLoader |
| `data/modelnet40/` | 数据集（未提交到 git 的大文件） |
| `figure_training_curve.png` | 训练曲线：200 epoch，平台期 0.86–0.87 |
| 其余 `*.py` | d2l 课程练习（softmax / MLP / LeNet / ResNet 等），非本项目主体 |

## 如何运行

```bash
python pointnet.py     # 训练 + 每 epoch 评估；结束时保存训练曲线
```

依赖：`torch`、`numpy`、`matplotlib`、`d2l`（`.venv` 已装，且 CUDA 可用）。
