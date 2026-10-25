#mesh_stats
import numpy as np
from collections import Counter
from scipy.sparse import coo_matrix
from scipy.sparse.csgraph import connected_components

def edge_counts(faces):
    e_count = Counter()
    for f in faces:
        for u, v in zip(f, f[1:] + f[:1]):
            e_count[(min(u, v), max(u, v))] += 1
    n_e = len(e_count)
    return e_count

def boundary_loops(e_count, n_v):
    boundary = [e for e, c in e_count.items() if c == 1]

    if not boundary:
        return 0, 0
    
    bu = np.array([e[0] for e in boundary])
    bv = np.array([e[1] for e in boundary])
    ones = np.ones(len(boundary))
    B = coo_matrix((ones, (bu, bv)), shape=(n_v, n_v))
    _, labels = connected_components(B, directed=False)
    deg = Counter()
    for u, v in boundary:
        deg[u] += 1
        deg[v] += 1
    n_loop = len({labels[v] for v in deg})
    n_bad = sum(1 for d in deg.values() if d != 2)

    return n_loop, n_bad

def mesh_stats_arrays(verts, faces):
    #v, f, e
    n_v = len(verts)
    n_f = len(faces)
    e_count = edge_counts(faces)
    n_e = len(e_count)
    chi = n_v - n_e + n_f
    #maniford edge
    dist = Counter(e_count.values())
    n_bound = dist.get(1, 0)
    n_inner = dist.get(2, 0)
    n_nonman = sum(c for k,  c in dist.items() if k >= 3)

    #vertices map from edge
    eu = []
    ev = []
    for e in e_count:
        eu.append(e[0])
        ev.append(e[1])
    ones = np.ones(n_e)
    G = coo_matrix((ones, (eu, ev)), shape=(n_v, n_v))
    n_comp, labels = connected_components(G, directed=False)
    v_c = np.bincount(labels,minlength=n_comp)
    e_c = np.bincount(labels[np.array(eu)], minlength=n_comp)
    f_c = np.bincount(np.array([labels[fc[0]] for fc in faces]), minlength=n_comp)
    chi_c = v_c - e_c + f_c

    n_loop, n_bad = boundary_loops(e_count, n_v)

    return {'V':n_v, 'E': n_e, "F": n_f,
            'chi': chi, "components": n_comp,
             'boundary_edges': n_bound,
             'boundary_loops': n_loop,
             'bad_boundary_vertices': n_bad,
             'interior_edges': n_inner,
             'nonmanifold_edges': n_nonman,
             'chi_per_component': chi_c}

