import numpy as np
import halfedge as he

def icosphere(sub=0, R=1.0):
    #points
    phi = (1 + np.sqrt(5)) / 2
    a = 1
    b = phi
    c = 0
    p_c = []
    for i in range(3):
        p = np.zeros(3)
        p[i] = a
        p[(i+1) % 3] = b
        p[(i+2) % 3] = c
        p_c.append((p))
        p = np.zeros(3)
        p[i] = -a
        p[(i+1) % 3] = b
        p_c.append((p))
        p = np.zeros(3)
        p[i] = a
        p[(i+1) % 3] = -b
        p_c.append((p))
        p = np.zeros(3)
        p[i] = -a
        p[(i+1) % 3] = -b
        p_c.append((p))

    p_c = np.array(p_c)
    p_c = R * p_c / np.linalg.norm(p_c, axis=1, keepdims=True)

    #faces
    def cal_face(pts):
        n = len(pts)
        A = np.zeros((n, n), dtype=bool)
        for i in range(n):
            dis = np.linalg.norm((pts[i] - pts), axis=1)
            idx = np.argsort(dis)
            near_idx = idx[1:6]
            A[i, near_idx] = True

        edges = np.argwhere(np.triu(A, 1))

        faces = set()
        for a, b in edges:
            for k in (np.where(A[a] & A[b])[0]):
                faces.add(tuple(sorted((a, b, k))))

        faces_sort = []
        for f in faces:
            i, j, k = f[0], f[1], f[2]
            a, b, c = pts[i], pts[j], pts[k]
            normal = np.cross(b-a, c-a)
            g = (a + b + c) / 3
            if np.dot(normal, g) < 0:
                faces_sort.append((i, k, j))
            else:
                faces_sort.append((i, j, k))

        return faces_sort

    
    faces = cal_face(p_c)
    return p_c, faces
