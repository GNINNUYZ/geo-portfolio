#kdtree
#(N, 3)point cloud

import numpy as np

import heapq



LEAF = 16
class KDNode:
    def __init__(self, pt, i, left=None, right=None):
        self.pt, self.i, self.left, self.right = pt, i, left, right

def build(points, idx=None, depth=0):
    if idx is None:
        idx = np.arange(len(points))
    n = len(idx)
    if n == 0:
        return None
    if n <= LEAF:
        return idx.copy()
    
    axis = depth % 3
    k = n // 2

    idx[:] = idx[np.argpartition(points[idx, axis], k)]

    node = KDNode(points[idx[k]], idx[k])
    node.left = build(points, idx[:k], depth + 1)
    node.right = build(points, idx[k + 1:], depth + 1)
    return node

def kNN(tree, points, query, k):
    heap = []

    def search(node, depth):
        if node is None:
            return

        if isinstance(node, np.ndarray):
            for i in node:
                d2 = ((points[i] - query) ** 2).sum()
                heapq.heappush(heap, (-d2, i))
                if len(heap) > k:
                    heapq.heappop(heap)
            return
        
        axis = depth % 3
        if query[axis] < node.pt[axis]:
            near, far = node.left, node.right
        else:
            near, far = node.right, node.left

        search(near, depth + 1)

        d2 = ((node.pt - query) ** 2).sum()
        heapq.heappush(heap, (-d2, node.i))
        if len(heap) > k:
            heapq.heappop(heap)

        if len(heap) < k or abs(query[axis] - node.pt[axis]) **2 < -heap[0][0]:
            search(far, depth + 1)

    search(tree, 0)
    return [i for _, i in heap]

def brute_force_knn(pts, query, k):
    d2 = ((pts - query) ** 2).sum(axis = 1)
    idx = np.argpartition(d2, k)[:k]
    return sorted(idx.tolist())

def radius_search(node, query, r, depth, heap):
    if node is None:
        return heap
    if isinstance(node, np.ndarray):
        for i in node:
            d2 = ((pts[i] - query)**2).sum()
            if d2 < r**2:
                heapq.heappush(heap, (-d2, i))
        return heap

    axis = depth % 3
    if query[axis] < node.pt[axis]:
        near, far = node.left, node.right
    else:
        near, far = node.right, node.left

    heap = radius_search(near, query, r, depth + 1, heap)

    d2 = ((node.pt - query) ** 2).sum()
    if d2 < r**2:
        heapq.heappush(heap, (-d2, node.i))
    if (query[axis] - node.pt[axis])**2 < r**2:
        radius_search(far, query, r, depth + 1, heap)
    return heap

def brute_radius_search(pts, query, r, heap):
    d2 =  ((pts - query)**2).sum(axis=1)
    idx =np.argwhere(d2 < r**2).ravel()
    return sorted(idx.tolist())