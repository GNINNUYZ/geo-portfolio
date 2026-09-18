import numpy as np
import torch
from torch import nn
from torch.nn import functional as F
from d2l import torch as d2l
from torch.utils.data import TensorDataset, DataLoader, Dataset
import os
import matplotlib.pyplot as plt

#输入点云
from provider import train_loader, test_loader

#T-net对齐
class TNet3(nn.Module):
    def __init__(self, k = 3):
        super().__init__()
        self.mlp = nn.Sequential(
            nn.Conv1d(k, 64, 1), nn.BatchNorm1d(64), nn.ReLU(),
            nn.Conv1d(64, 128, 1), nn.BatchNorm1d(128), nn.ReLU(),
            nn.Conv1d(128, 256, 1), nn.BatchNorm1d(256), nn.ReLU(),
        )
        self.fc = nn.Sequential(
            nn.Linear(256, 512), nn.BatchNorm1d(512), nn.ReLU(),
            nn.Linear(512, 256), nn.BatchNorm1d(256), nn.ReLU(),
            nn.Linear(256, k * k),
        )
        self.k = k

    def forward(self, x):
        x = self.mlp(x)
        x = x.amax(dim=2)
        x = self.fc(x)
        identity= torch.eye(self.k).to(x.device).view(1, -1)
        return x + identity
#shared MLP
shared_mlp_1 = nn.Sequential(nn.Conv1d(3, 64, 1),
                            nn.BatchNorm1d(64),
                            nn.ReLU(),
                            nn.Conv1d(64, 64, 1),
                            nn.BatchNorm1d(64),
                            nn.ReLU(),)
#T-NET(64)
class TNet64(nn.Module):
    def __init__(self, k = 64):
        super().__init__()
        self.mlp = nn.Sequential(
            nn.Conv1d(k, 128, 1), nn.BatchNorm1d(128), nn.ReLU(),
            nn.Conv1d(128, 256, 1), nn.BatchNorm1d(256), nn.ReLU(),
            nn.Conv1d(256, 512, 1), nn.BatchNorm1d(512), nn.ReLU(),
        )
        self.fc = nn.Sequential(
            nn.Linear(512, 256), nn.BatchNorm1d(256), nn.ReLU(),
            nn.Linear(256, 256), nn.BatchNorm1d(256), nn.ReLU(),
            nn.Linear(256, k * k),
        )
        self.k = k

    def forward(self, x):
        x  = self.mlp(x)
        x = x.amax(dim=2)
        x = self.fc(x)
        identity= torch.eye(self.k).to(x.device).view(1, -1)
        return x + identity
#shared MLP
shared_mlp_2 = nn.Sequential(nn.Conv1d(64, 128, 1),
                            nn.BatchNorm1d(128),
                            nn.ReLU(),
                            nn.Conv1d(128, 256, 1),
                            nn.BatchNorm1d(256),
                            nn.ReLU(),
                            nn.Conv1d(256, 1024, 1),
                            nn.BatchNorm1d(1024),
                            nn.ReLU(),)
#Maxpool dim=2
#FC + dropout +BN
head = nn.Sequential(
    nn.Linear(1024,512), nn.BatchNorm1d(512), nn.ReLU(), nn.Dropout(0.3),
    nn.Linear(512,256), nn.BatchNorm1d(256), nn.ReLU(), nn.Dropout(0.3),
    nn.Linear(256, 40),)

class PointNet(nn.Module):
    def __init__(self, num_classes=40):
        super().__init__()
        self.tnet3 = TNet3()
        self.tnet64 = TNet64()
        self.mlp1 = shared_mlp_1
        self.mlp2 = shared_mlp_2
        self.head = head

    def forward(self, x):
        a1 = self.tnet3(x).view(-1, 3, 3)
        x = torch.bmm(x.transpose(1, 2), a1).transpose(1, 2)
        x = self.mlp1(x)
        a2 = self.tnet64(x).view(-1, 64, 64)
        x = torch.bmm(x.transpose(1, 2), a2).transpose(1, 2)
        x = self.mlp2(x)
        x=x.amax(dim=2)
        return self.head(x), a2

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
net = PointNet(40).to(device)
optimizer = torch.optim.Adam(net.parameters(), lr = 0.001)
loss_fn = nn.CrossEntropyLoss()
scheduler = torch.optim.lr_scheduler.StepLR(optimizer, step_size=20, gamma=0.5)
def ortho_loss(A):
    I = torch.eye(64, device=A.device)
    return F.mse_loss(A @ A.transpose(1, 2), I.expand_as(A))

accs = []

for epoch in range(200):
    net.train()
    for xb, yb in train_loader:
        xb, yb = xb.to(device), yb.to(device)
        out, a2 = net(xb)
        cls_loss =loss_fn(out , yb)
        loss = cls_loss + 0.001 * ortho_loss(a2)
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

    net.eval()
    correct = total = 0
    with torch.no_grad():
        for xb, yb in test_loader:
            xb, yb = xb.to(device), yb.to(device)
            out, _ = net(xb)
            correct += (out.argmax(dim=1) == yb).sum().item()
            total += yb.size(0)

    accs.append(correct / total)
    scheduler.step()
    print(f'epoch {epoch}: loss {loss.item():.4f}  acc{correct/total:.4f}')


plt.plot(accs)
plt.xlabel('epoch')
plt.ylabel('acc %')
script_path = os.path.dirname(__file__)
plt.savefig(os.path.join(script_path, 'pointnet_acc.png'))
plt.show()