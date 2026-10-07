#orientation
import numpy as np
#pca_normal#
normal = []
def kNN(tree, pts, query, k=10):
    pass
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

pts = []
idx = np.arange(len(pts))
query = pts[0]
tree = kNN.build()
line = []
keys = set()
#MST
k=10
for i in idx:
    near_idx = kNN(tree, pts, pts[i], k)
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
