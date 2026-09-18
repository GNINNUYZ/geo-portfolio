import numpy as np
import os
from torch.utils.data import TensorDataset, DataLoader, Dataset
import torch

data_dir = 'data/modelnet40/ModelNet40'
n_points = 1024

def read_off(path):
    with open(path) as f:
        lines = f.readlines()
        if lines[0].upper().startswith('OFF') and len(lines[0].strip()) > 3:
            lines = ['OFF\n'] + [lines[0][3:]] + lines[1:]
        n_verts, n_faces, _ = map(int, lines[1].split())

        verts = np.array(
            [list(map(float, l.split())) for l in lines[2:2 + n_verts]],
            dtype=np.float32,
        )

        faces = np.array(
            [list(map(int, l.split()[1:])) for l in lines[2 + n_verts : 2 + n_verts + n_faces]],
            dtype=np.int64,
        )
        return verts, faces

def sample_points(verts, faces, n = n_points, rng=np.random.default_rng()):
    v0 = verts[faces[:, 0]]
    v1 = verts[faces[:, 1]]
    v2 = verts[faces[:, 2]]

    areas = np.linalg.norm(np.cross((v1 -v0).astype(np.float64), (v2 - v0).astype(np.float64)), axis=1) / 2

    idx = rng.choice(len(faces), n, p = areas / areas.sum())

    v0, v1, v2 = v0[idx], v1[idx], v2[idx]

    u = rng.random(n)
    w = rng.random(n)
    s = np.sqrt(u)

    pts = (1 - s)[:, None] * v0 + (s * (1 - w))[:, None] *v1 + (s * w)[:,None] * v2
    return pts

def normalize(pc):
    pc = pc - pc.mean(axis=0)
    pc = pc / np.max(np.linalg.norm(pc, axis=1))
    return pc

class ModelNet40(Dataset):
    def __init__(self, split='train', cache=True):
        super().__init__()
        self.classes = sorted(os.listdir(data_dir))
        self.files = []
        self.labels = []
        for cid, c in enumerate(self.classes):
            d = os.path.join(data_dir, c, split)
            for fn in sorted(os.listdir(d)):
                self.files.append(os.path.join(d, fn))
                self.labels.append(cid)
        self.cache = cache
        self.pts_cache = {}

    def __len__(self):
        return len(self.files)

    def __getitem__(self, index):
        if index not in self.pts_cache:
            verts, faces = read_off(self.files[index])
            self.pts_cache[index] = normalize(sample_points(verts, faces))

        pts = self.pts_cache[index]
        return torch.tensor(pts.T, dtype=torch.float32), self.labels[index]

train_ds = ModelNet40('train')
test_ds = ModelNet40('test')

train_loader = DataLoader(train_ds, batch_size=128, shuffle=True)
test_loader = DataLoader(test_ds, batch_size=128)

if __name__ == '__main__':
    xb, yb = next(iter(train_loader))
    print(xb.shape)
    print(yb.shape)