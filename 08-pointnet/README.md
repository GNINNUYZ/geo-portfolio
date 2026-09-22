# ML — PointNet 复现（ModelNet40 分类）

从论文实现 PointNet（[Qi et al., 2017](https://arxiv.org/abs/1612.00593)），在 ModelNet40 上做 40 类形状分类。
本 README 按仓库约定补齐：**背景 / 数据 / 方法 / 结果（数字）/ 如何运行**。

## 结果

| 指标 | 值 |
|---|---|
| ModelNet40 test accuracy（best） | **0.8679**（epoch 43，2026-09-22 运行） |
| 末轮 accuracy | 0.8497（epoch 199）—— 峰值后有明显退化 |
| 训练轮数 | **200 epoch，无提前停止** |
| 总训练耗时 | **2692.96 s ≈ 44.9 分钟**（首轮 765 s，其后约 9 s/轮） |
| 10 epoch 时 | ~81.7%（中间结果，**不再引用**） |
| 训练设备 | NVIDIA RTX 5060 Ti 16 GB（`.venv` 内 torch 2.12.1+cu130，`cuda.is_available() == True`） |

**训练曲线**：`pointnet_acc.png` —— 横轴 0→199 epoch。**峰值 0.8679 出现在 epoch 43，之后逐步回落到末轮 0.8497**；200 轮中 47 轮 >0.85。
> 口径：**86%（取 best，= 0.8679）**，与 CV 及动机信一致；81.7% 是 10 epoch 的中间结果，作废。
> ⚠️ 注意"峰值 vs 末值"的差别：本 README 早期版本写作"约 50 epoch 后稳定在 0.86–0.87"，
> 但**逐 epoch 日志显示峰值后是回落、不是稳定**（epoch 100 之后多在 0.84–0.85）。
> 引 86% 时应说明它是 **best**，不是最终值。

**训练日志**：`train_log.txt` —— 每 epoch 一行（`epoch / loss / acc / 单轮耗时`），末行为汇总
（`best acc` / `best epoch` / 总耗时 / GPU）。这是 86% 的可核实证据（2026-09-22 补）。

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
| `pointnet.py` | 模型定义 + 训练循环（含正交正则、测试集评估、曲线与日志落盘） |
| `provider.py` | ModelNet40 读取（OFF 解析）、面积加权采样、单位球归一化、DataLoader |
| `data/modelnet40/` | 数据集（未提交到 git 的大文件，9.3 GB） |
| `pointnet_acc.png` | 训练曲线（2026-09-22 运行）：峰值 0.8679 @ epoch 43，末轮 0.8497 |
| `train_log.txt` | 逐 epoch 日志 + 末行汇总（best acc / best epoch / 总耗时 / GPU） |
| 其余 `*.py` | d2l 课程练习（softmax / MLP / LeNet / ResNet 等），非本项目主体 |

## 如何运行

```bash
cd 08-pointnet
python pointnet.py     # 训练 + 每 epoch 评估；写 train_log.txt 并保存训练曲线
```

**Interpreter:** `.venv`（Python 3.11 + torch 2.12.1+cu130）。注意 **Anaconda 环境没有 torch**。
数据路径是相对路径 `data/modelnet40/ModelNet40`，所以**必须在 `08-pointnet/` 下运行**
（`08-pointnet/data/` 已在 `.gitignore` 中，不进仓库）。

依赖：`torch`、`numpy`、`matplotlib`、`d2l`。
