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

    def getmid(pts, a, b):
        mid = (pts[a] + pts[b]) / 2
        return mid
    
    def subd(pts, faces):
        mid = {}
        newP = list(pts)
        for f in faces:
            for (u, v) in zip(f, f[1:] + f[:1]):
                sp = u
                ep = v
                key = (min(sp,ep),max(sp,ep))
                if key not in mid:
                    m = getmid(pts, sp, ep)
                    m = R * m / np.linalg.norm(m)
                    mid[key] = len(newP)
                    newP.append(m)
        subd_faces = []
        for f in faces:
            a, b, c = f[0], f[1], f[2]
            subd_faces.append((a, mid[min(a, b), max(a, b)], mid[min(c, a), max(c, a)]))
            subd_faces.append((b, mid[min(b, c), max(b, c)], mid[min(a, b), max(a, b)]))
            subd_faces.append((c, mid[min(c, a), max(c, a)], mid[min(b, c), max(b, c)]))
            subd_faces.append((mid[min(a, b), max(a, b)], mid[min(b, c), max(b, c)], mid[min(c, a), max(c, a)]))
        return np.array(newP), subd_faces

    for _ in range(sub):
        p_c, faces = subd(p_c, faces)
    return p_c, faces

if __name__ == "__main__":
    p, f = icosphere(sub=1)
    print(len(p), len(f))