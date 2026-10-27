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

def build_link(n_v, faces):
    link = [[] for _ in range(n_v)]

    #half-edge
    for face in faces:
        n = len(face)
        for k, v in enumerate(face):
            prev = face[k-1]
            nxt = face[(k+1) % n]
            link[v].append((prev, nxt))
    return link

def nonmanifold_vertices(n_v, faces) -> list:
    link = build_link(n_v, faces)
    bad = []

    for v in range(n_v):
        edges = link[v]

        if not edges:
            continue
        parent = {}

        def find(x):
            parent.setdefault(x, x)
            while parent[x] != x:
                x = parent[x]
            return x

        def union(a, b):
            ra = find(a)
            rb = find(b)
            if ra != rb:
                parent[ra] = rb

        deg = Counter()
        for (a, b) in edges:
            union(a, b)
            deg[a] += 1
            deg[b] += 1

        n_pieces= len({find(x) for x in parent})

        max_deg = max(deg.values())

        if n_pieces > 1 or max_deg > 2:
            bad.append(v)
    
    return bad

def degenerate_faces(verts, faces):
    verts = np.asarray(verts, dtype=float)
    ext = np.linalg.norm(verts.max(axis=0) - verts.min(axis=0))
    eps = 1e-12 * ext**2

    bad = []
    for fi, f in enumerate(faces):
        if len(set(f)) != len(f):
            bad.append(fi)
            continue

        p = [verts[i] for i in f]
        m = len(p)
        nrm = sum(np.cross(p[k], p[(k+1)%m]) for k in range(m))
        area = 0.5 * np.linalg.norm(nrm)

        if area < eps:
            bad.append(fi)
        
    return bad

        
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
    nonman = nonmanifold_vertices(n_v, faces)
    degen = degenerate_faces(verts, faces)

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
    
    directed = Counter()
    for f in faces:
        for u, v in zip(f, f[1:] + f[:1]):
            directed[u, v] += 1

    is_oriented = not any(c >= 2 for c in directed.values())
    

    return {'V':n_v, 'E': n_e, "F": n_f,
            'chi': chi, "components": n_comp,
             'boundary_edges': n_bound,
             'boundary_loops': n_loop,
             'bad_boundary_vertices': n_bad,
             'interior_edges': n_inner,
             'nonmanifold_edges': n_nonman,
             'chi_per_component': chi_c,
             'nonmanifold_vertices': nonman,
             'is_manifold': (n_nonman == 0 and len(nonman) == 0),
             'degenerate_faces': degen,
            'is_closed': n_bound == 0,
            'is_oriented': is_oriented
             }
