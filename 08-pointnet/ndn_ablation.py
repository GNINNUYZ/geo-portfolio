# -*- coding: utf-8 -*-
"""
辩证持续学习（NDN）完整实现 + 消融实验
任务：MNIST 0-4 -> 5-9（10 类共享输出头，真遗忘场景）

方法对比（均先学 A 作为正题）:
  1. baseline   : 直接学 B（无保护）
  2. ewc        : 防御式——EWC 正则锁旧权重
  3. antithesis : 反题——学 B 同时对 A 梯度上升（主动破坏）
  4. synthesis  : 合题——学 B + 蒸馏恢复 A（无反题）
  5. ndn        : 反题 + 合题（完整辩证闭环）

关键消融: ndn vs synthesis
  → 先破坏再综合 ≈ 直接综合   : 反题无增益，叙事崩
  → 先破坏再综合 > 直接综合   : 否定非平凡（呼应 Forgetting-to-Learn 思路）

设计要点:
  - 10 类共享输出头、B 用真实标签 5-9：A/B 目标才有冲突、才会遗忘。
    若把 5-9 重映射到 0-4，数字 0 和数字 5 都指向输出 0，模型可同时答对，
    测不出灾难性遗忘，消融判读无意义。
  - synthesis/ndn 只在 A 样本上蒸馏：teacher 没见过 B，对 B 输出近均匀，
    B 侧 KD 只是熵正则化，会压低 B 精度。
"""
import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
from torchvision import datasets, transforms
from torch.utils.data import DataLoader, Subset
import numpy as np
import random
import itertools
import copy

# ---------- 配置 ----------
SEEDS     = [42, 2024, 7]   # 多次种子取均值±std（想快只留 [42]）
LR_A      = 0.001
EPOCHS_A  = 5
LR_B      = 0.001
EPOCHS_B  = 5
ALPHA     = 0.3      # 反题强度：对 A 梯度上升系数
LAMBDA_EWC = 1000.0  # EWC 正则强度
LAMBDA_D  = 0.5      # 蒸馏强度
TEMP      = 3.0      # 蒸馏温度
BATCH     = 128
device    = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print("设备:", device)


# ---------- 固定随机种子 ----------
def set_seed(seed=42):
    torch.manual_seed(seed)
    np.random.seed(seed)
    random.seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed)


# ---------- 数据准备 ----------
transform = transforms.Compose([
    transforms.ToTensor(),
    transforms.Normalize((0.1307,), (0.3081,))
])

full_train = datasets.MNIST(root='./data', train=True, download=True, transform=transform)
full_test  = datasets.MNIST(root='./data', train=False, download=True, transform=transform)


def get_task_data(dataset, labels):
    idx = [i for i, (x, y) in enumerate(dataset) if y in labels]
    return Subset(dataset, idx)


train_A = get_task_data(full_train, range(5))
train_B = get_task_data(full_train, range(5, 10))   # 真实标签 5-9，10 类头
test_A  = get_task_data(full_test,  range(5))
test_B  = get_task_data(full_test,  range(5, 10))

loader_A = DataLoader(train_A, batch_size=BATCH, shuffle=True)
loader_B = DataLoader(train_B, batch_size=BATCH, shuffle=True)
test_loader_A = DataLoader(test_A, batch_size=BATCH, shuffle=False)
test_loader_B = DataLoader(test_B, batch_size=BATCH, shuffle=False)


# ---------- 网络 ----------
class MLP(nn.Module):
    def __init__(self, input_dim=784, hidden=256, num_classes=10):
        super().__init__()
        self.fc1 = nn.Linear(input_dim, hidden)
        self.fc2 = nn.Linear(hidden, hidden)
        self.fc3 = nn.Linear(hidden, num_classes)

    def forward(self, x):
        x = x.view(x.size(0), -1)
        h1 = torch.relu(self.fc1(x))
        h2 = torch.relu(self.fc2(h1))
        return self.fc3(h2), h2


# ---------- 评估 ----------
def evaluate(model, loader):
    model.eval()
    correct, total = 0, 0
    with torch.no_grad():
        for x, y in loader:
            x, y = x.to(device), y.to(device)
            logits, _ = model(x)
            _, pred = torch.max(logits, 1)
            correct += (pred == y).sum().item()
            total += y.size(0)
    return correct / total


def evaluate_both(model):
    acc_A = evaluate(model, test_loader_A)
    acc_B = evaluate(model, test_loader_B)
    return acc_A, acc_B, (acc_A + acc_B) / 2


# ---------- 1. 标准训练（正题 / baseline）----------
def train_ce(model, loader, epochs, lr):
    model.to(device)
    model.train()
    optimizer = optim.Adam(model.parameters(), lr=lr)
    for epoch in range(epochs):
        for x, y in loader:
            x, y = x.to(device), y.to(device)
            optimizer.zero_grad()
            logits, _ = model(x)
            loss = F.cross_entropy(logits, y)
            loss.backward()
            optimizer.step()


# ---------- 2. EWC（防御式）----------
def compute_fisher(model, loader):
    """Fisher 估计。注意：每 batch 先 zero_grad，否则梯度跨 batch 累积，全是垃圾。"""
    model.eval()
    grads = {name: torch.zeros_like(p) for name, p in model.named_parameters() if p.requires_grad}
    for x, y in loader:
        x, y = x.to(device), y.to(device)
        model.zero_grad()
        logits, _ = model(x)
        loss = F.cross_entropy(logits, y)
        loss.backward()
        for name, p in model.named_parameters():
            if p.grad is not None:
                grads[name] += p.grad.detach() ** 2
    for name in grads:
        grads[name] /= len(loader)
    return grads


def train_ewc(model, loader, epochs, lr, fisher, opt_weights, lambd):
    model.train()
    optimizer = optim.Adam(model.parameters(), lr=lr)
    for epoch in range(epochs):
        for x, y in loader:
            x, y = x.to(device), y.to(device)
            optimizer.zero_grad()
            logits, _ = model(x)
            loss = F.cross_entropy(logits, y)
            for n, p in model.named_parameters():
                loss += (lambd / 2) * (fisher[n] * (p - opt_weights[n]) ** 2).sum()
            loss.backward()
            optimizer.step()


# ---------- 3. 反题：对 A 梯度上升 ----------
def train_antithesis(model, loader_b, loader_a, epochs, lr, alpha):
    """loss = CE(B) - alpha * CE(A)：B 正常学，A 被主动破坏。"""
    model.train()
    optimizer = optim.Adam(model.parameters(), lr=lr)
    cyc_a = itertools.cycle(loader_a)
    for epoch in range(epochs):
        for xb, yb in loader_b:
            xa, ya = next(cyc_a)
            xb, yb, xa, ya = xb.to(device), yb.to(device), xa.to(device), ya.to(device)
            optimizer.zero_grad()
            logits_b, _ = model(xb)
            loss_b = F.cross_entropy(logits_b, yb)
            logits_a, _ = model(xa)
            loss_a = F.cross_entropy(logits_a, ya)
            loss = loss_b - alpha * loss_a          # 梯度上升 = 主动遗忘 A
            loss.backward()
            optimizer.step()


# ---------- 4. 合题：蒸馏恢复 A ----------
def kd_loss(logits_s, logits_t, temp):
    """KL(student||teacher)，温度缩放。"""
    return F.kl_div(F.log_softmax(logits_s / temp, dim=1),
                    F.softmax(logits_t / temp, dim=1),
                    reduction='batchmean') * temp ** 2


def train_synthesis(model, loader_b, loader_a, epochs, lr, teacher, lam_d, temp):
    """B 样本: 纯 CE（teacher 没见过 B，B 侧 KD 只是熵正则，会压 B 精度）。
       A 样本: 纯蒸馏锚点（无 CE，避免重训 A）。"""
    model.train()
    teacher.eval()
    optimizer = optim.Adam(model.parameters(), lr=lr)
    cyc_a = itertools.cycle(loader_a)
    for epoch in range(epochs):
        for xb, yb in loader_b:
            xa, _ = next(cyc_a)
            xb, yb, xa = xb.to(device), yb.to(device), xa.to(device)
            optimizer.zero_grad()
            logits_b, _ = model(xb)
            loss = F.cross_entropy(logits_b, yb)
            with torch.no_grad():
                t_a, _ = teacher(xa)
            logits_a, _ = model(xa)
            loss += lam_d * kd_loss(logits_a, t_a, temp)   # A 锚点，只蒸馏不打标签
            loss.backward()
            optimizer.step()


# ---------- 方法入口 ----------
def run_method(method, seed):
    set_seed(seed)
    log = {}

    # 正题：学 A
    model_A = MLP().to(device)
    train_ce(model_A, loader_A, EPOCHS_A, LR_A)
    acc_A0, _, _ = evaluate_both(model_A)
    teacher = copy.deepcopy(model_A)          # 正题产物 = 蒸馏 teacher（冻结）

    m = copy.deepcopy(model_A)

    if method == 'baseline':
        train_ce(m, loader_B, EPOCHS_B, LR_B)

    elif method == 'ewc':
        fisher = compute_fisher(model_A, loader_A)
        opt_weights = {n: p.detach().clone() for n, p in model_A.named_parameters()}
        train_ewc(m, loader_B, EPOCHS_B, LR_B, fisher, opt_weights, LAMBDA_EWC)

    elif method == 'antithesis':
        train_antithesis(m, loader_B, loader_A, EPOCHS_B, LR_B, ALPHA)

    elif method == 'synthesis':
        train_synthesis(m, loader_B, loader_A, EPOCHS_B, LR_B, teacher, LAMBDA_D, TEMP)

    elif method == 'ndn':
        # 反题（一半预算，破坏 A 同时学 B）
        train_antithesis(m, loader_B, loader_A, EPOCHS_B // 2, LR_B, ALPHA)
        acc_A_destroyed, _, _ = evaluate_both(m)
        log['反题后 A（应暴跌）'] = acc_A_destroyed
        # 合题（一半预算，蒸馏恢复 A）
        train_synthesis(m, loader_B, loader_A, EPOCHS_B - EPOCHS_B // 2, LR_B, teacher, LAMBDA_D, TEMP)

    acc_A, acc_B, avg = evaluate_both(m)
    return {
        'acc_A0': acc_A0, 'acc_A': acc_A, 'acc_B': acc_B, 'avg': avg,
        'bwt': acc_A - acc_A0,   # 后向迁移：负 = 遗忘
        'log': log,
    }


# ---------- 主循环 ----------
METHODS = ['baseline', 'ewc', 'antithesis', 'synthesis', 'ndn']
results = {m: [] for m in METHODS}

for seed in SEEDS:
    print(f"\n===== seed={seed} =====")
    for m in METHODS:
        r = run_method(m, seed)
        results[m].append(r)
        extra = f" | 反题后A={r['log']['反题后 A（应暴跌）']:.4f}" if '反题后 A（应暴跌）' in r['log'] else ""
        print(f"  {m:<10} A0={r['acc_A0']:.4f} A={r['acc_A']:.4f} B={r['acc_B']:.4f} "
              f"avg={r['avg']:.4f} BWT={r['bwt']:+.4f}{extra}")


# ---------- 汇总（均值±std）----------
print("\n" + "=" * 72)
print(f"{'方法':<12}{'A(学B后)':<22}{'B':<16}{'avg':<16}{'BWT':<16}")
print("-" * 72)
summ = {}
for m in METHODS:
    rs = results[m]
    def ms(key):
        vals = [r[key] for r in rs]
        return f"{np.mean(vals):.4f}±{np.std(vals):.4f}"
    summ[m] = (np.mean([r['acc_A'] for r in rs]), np.mean([r['acc_B'] for r in rs]))
    print(f"{m:<12}{ms('acc_A'):<22}{ms('acc_B'):<16}{ms('avg'):<16}{ms('bwt'):<16}")

# 关键消融判读
print("\n" + "=" * 72)
print("消融判读（看均值）:")
print(f"  ndn       A={summ['ndn'][0]:.4f}  B={summ['ndn'][1]:.4f}")
print(f"  synthesis A={summ['synthesis'][0]:.4f}  B={summ['synthesis'][1]:.4f}")
print(f"  antithesis 单独: 反题无合题 = 主动遗忘的代价")
if summ['ndn'][0] > summ['synthesis'][0] + 0.005 or summ['ndn'][1] > summ['synthesis'][1] + 0.005:
    print("  -> ndn > synthesis：反题有增益，辩证闭环成立（主要结论）")
elif abs(summ['ndn'][0] - summ['synthesis'][0]) < 0.005 and abs(summ['ndn'][1] - summ['synthesis'][1]) < 0.005:
    print("  -> ndn ≈ synthesis：反题无增益，跳过反题直接合题即可（叙事风险，如实报告）")
else:
    print("  -> ndn < synthesis：反题有害，辩证叙事不成立（诚实报告，同样有价值）")
