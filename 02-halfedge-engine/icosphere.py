import numpy as np
import halfedge as he

def icosphere(sub=0, R=1.0):
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

    return p_c