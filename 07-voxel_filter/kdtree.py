#kdtree
#(N, 3)point cloud
import os
import numpy as np
import laspy
import heapq
import time

scr_path = os.path.dirname(__file__)
data_path = os.path.join(scr_path, '..', 'data', 'small_dutch.laz')
with laspy.open(data_path) as f:
    las = f.read()

    pts = las.xyz
    print(len(pts))
    LEAF = 16
    class KDNode:
        def __init__(self, pt, i, left=None, right=None):
            self.pt, self.i, self.left, self.right = pt, i, left, right

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
        return KDNode(pts[idx[k]], idx[k], left, right)

    tree = build(np.arange(len(pts)))

    def kNN(node, query, k, depth, heap):
        if node is None:
            return heap

        if isinstance(node, np.ndarray):
            for i in node:
                d2 = ((pts[i] - query) ** 2).sum()
                heapq.heappush(heap, (-d2, i))
                if len(heap) > k:
                    heapq.heappop(heap)
            return heap

        axis = depth % 3
        if query[axis] < node.pt[axis]:
            near, far = node.left, node.right
        else:
            near, far = node.right, node.left

        heap = kNN(near, query, k, depth + 1, heap)

        d2 = ((node.pt - query) ** 2).sum()
        heapq.heappush(heap, (-d2, node.i))
        if len(heap) > k:
            heapq.heappop(heap)

        if len(heap) < k or abs(query[axis] - node.pt[axis]) **2 < -heap[0][0]:
            heap = kNN(far, query, k, depth +1, heap)

        return heap

    def brute_force_knn(pts, query, k):
        d2 = ((pts - query) ** 2).sum(axis = 1)
        idx = np.argpartition(d2, k)[:k]
        return sorted(idx.tolist())

    query = pts[len(pts) // 2]
    k = 5
    heap = kNN(tree, query, k, 0, [])
    tree_ids = sorted([i for _, i in heap])
    brute_ids = brute_force_knn(pts, query, k)

    print("tree:", tree_ids)
    print("tree:", brute_ids)
    print("match:", tree_ids == brute_ids)
        
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
    
    query = pts[len(pts) // 2]
    r = 5

    t0 = time.time()
    for _ in range(100):
        heap = radius_search(tree, query, r, 0, [])
        tree_ids = sorted(i for _, i in heap)
    t1 =time.time()
    for _ in range(100):
        brute_ids = brute_radius_search(pts, query, r, [])
    t2 = time.time()

    print("tree:", round(t1 - t0, 4), "s")
    print("brute:", round(t2 - t1, 4), "s")

    #print("tree:", tree_ids)
    #print("brute:", brute_ids)
    #print("match:", tree_ids == brute_ids)