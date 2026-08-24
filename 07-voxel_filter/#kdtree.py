#kdtree
#(N, 3)point cloud
import os
import numpy as np
import laspy

scr_path = os.path.dirname(__file__)
data_path = os.path.join(scr_path, '..', 'data', 'small_dutch.laz')
with laspy.open(data_path) as f:
    las = f.read()

    pts = las.xyz
    LEAF = 16
    class KDNode:
        def __init__(self, pt, left=None, right=None):
            self.pt, self.left, self.right = pt, left, right

    def build(idx, depth=0):
        n = len(idx)
        if n == 0:
            return None
        if n <= LEAF:
            return idx.copy()
        
        axis = depth % 3
        k = n // 2

        idx[:] = idx[np.argpartition(pts[idx, axis], k)]

        left = build(idx[:k], depth + 1)
        right = build(idx[k + 1:], depth + 1)
        return KDNode(pts[idx[k]], left, right)

    tree = build(np.arange(len(pts)))

    def kNN(node, query, k, depth, heap):
       
        if node == None:
            return best
        if query[axis] < pts[idx, axis]:
            kNN(node.left, query, best)

