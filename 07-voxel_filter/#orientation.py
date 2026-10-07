#orientation
import numpy as np
import kdtree

np.random.seed(42)
#pca_normal#
def compute_normals(points, k = 20):
    tree = kdtree.build(points)
    normal, eiglist = [], []
    for i in range(len(points)):
        idx = kdtree.kNN(tree, points, points[i], k)
        pts = points[idx]
        pts_cen = pts.mean(axis=0)
        X = pts - pts_cen
        H = X.T @ X
        eigvals, cov = np.linalg.eigh(H)
        normal.append(cov[:,0])
        eiglist.append(eigvals)
    return np.array(normal), np.array(eiglist)

#DSU
class DSU:
    def __init__(self,n):
        self.parent = np.arange(n)
        self.size = [1] * n ##integer
        self.comp = n

    def find(self, x):
        change_idx = []
        while self.parent[x] != x:
            x = self.parent[x]
        return self.parent[x]
    
    def union(self, a, b):
        ra = self.find(a)
        rb = self.find(b)
        if ra == rb:
            return False
        
        elif self.size[ra] <= self.size[rb]:
            self.parent[ra] = rb
            self.size[rb] += self.size[ra]
            self.comp -= 1
            return True
        else:
            self.parent[rb] = ra
            self.size[ra] += self.size[rb]
            self.comp -= 1
            return True

#make sphere
r = 100
theta = np.random.uniform(0, np.pi, 1000)
phi = np.random.uniform(0, 2*np.pi, 1000)
x = r * np.sin(theta) * np.cos(phi)
y = r * np.sin(theta) * np.sin(phi)
z = r * np.cos(theta)
sphere = np.column_stack([x, y, z])
normal_sph = sphere / r

pts = sphere
normal, eigvals = compute_normals(pts, k=20)
idx = np.arange(len(pts))
tree = kdtree.build(pts)
line = []
keys = set()
#MST
k=10
for i in idx:
    near_idx = kdtree.kNN(tree, pts, pts[i], k)
    for j in range(len(near_idx)):
        if i == near_idx[j]:
            continue
        elif i > near_idx[j]:
            low, high = near_idx[j], i
        else:
            low, high = i, near_idx[j]
        if low*len(pts) + high in keys:
            continue
        else:
            line.append((low, high))
            keys.add(low*len(pts) + high)

ls = []
le = []
for ele in line:
    ls.append(ele[0])
    le.append(ele[1])
ls = np.array(ls)
le = np.array(le)

ns = normal[ls]
ne = normal[le]

w = - np.abs((ns * ne).sum(axis=1)) + 1

line_w = np.column_stack((ls, le, w))
w_sort = np.argsort(w)
line_sort = np.column_stack((ls[w_sort], le[w_sort], w[w_sort]))

line_coherence = 0
for i in w_sort:
    if normal[ls[i]] @ normal[le[i]] >= 0:
        line_coherence += 1
line_coh_ratio = line_coherence / len(w_sort)
print(f'line coherence:{line_coh_ratio * 100}%')

#Kruskal
dsu = DSU(len(pts))
MST = []
for e in w_sort:
    a = ls[e]
    b = le[e]
    if dsu.union(a, b):
        MST.append(e)
    if len(MST) == len(pts) - 1:
        break

w_sum = np.array(w[MST])
print(f'dsu.comp:{dsu.comp}, MST length:{len(MST)}, weight sum:{w_sum.sum()}')

near_connect_sheet = [[] for _ in range(len(pts))]
for i in MST:
    a, b = ls[i], le[i]
    near_connect_sheet[a].append(b)
    near_connect_sheet[b].append(a) 

#view_point_method
vp = pts.mean(axis=0) + [0, 0, 300]
normal, eigvals = compute_normals(pts, k=20)
flip = 0
for i in idx:
    if normal[i] @ (vp - pts[i]) <= 0:
        normal[i] *= -1
        flip += 1

outter_normal_count = 0
for i in range(len(normal)):
    if normal[i] @ normal_sph[i] > 0:
        outter_normal_count += 1
outter_ratio = outter_normal_count / len(idx)
inward_ratio = 1 - outter_ratio
coherence = max(outter_ratio, inward_ratio)

visible_outter = 0
visible_p = 0
for i in idx:
    if normal_sph[i] @ (vp - pts[i]) > 0:
        visible_p += 1
        if normal[i] @ normal_sph[i] > 0:
            visible_outter += 1
visible_ratio = visible_outter / visible_p

print(f'outter normal percentage:{outter_normal_count}, filp percentage:{(flip/len(idx)) * 100}%, cohierence:{coherence * 100}%, visible coherence ratio:{visible_ratio * 100}%')