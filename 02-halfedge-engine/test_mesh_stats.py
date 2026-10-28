#test_mesh_stats
import numpy as np, sys
sys.path.insert(0, r'E:\ailearning\geo-portfolio\02-halfedge-engine')
from icosphere import icosphere
from mesh_stats import mesh_stats_arrays, degenerate_faces

def make_grid(n):
    verts = []
    pos = {}
    faces = []
    for i in range(n+1):
        for j in range(n+1):
            verts.append((i, j, 0.0))
            pos[(i, j)] = len(verts) - 1
    for i in range(n):
        for j in range(n):
            faces.append((pos[(i, j)], pos[(i+1, j)], pos[(i+1, j+1)], pos[(i, j+1)]))
    return np.array(verts), faces

def icosphere_0():
    return icosphere(sub=0)

def grid_5():
    return make_grid(5)

def two_spheres():
    v, f =icosphere(sub=0)
    vs = np.vstack([v, v*3])
    fs = list(f) + [(a+12, b+12, c+12) for a, b, c in f]
    return vs, fs

def bowtie():
    verts = np.zeros((5,3))
    faces = [(0, 1, 2), (0, 3, 4)]
    return verts, faces

def three_on_edge():
    verts = np.zeros((5, 3))
    faces = [(0,1,2),(0,1,3),(0,1,4)]
    return verts, faces

def reversed_face():
    v, f = icosphere(sub=0)
    f2 = list(f)
    f2[0] = tuple(reversed(f2[0]))
    return v, f2

def degen_repeat_vertex():
    verts = np.zeros((3,3))
    face = [(0, 0, 1)]
    return verts, face

def degen_collinear():
    verts = [[0,0,0],[1,0,0],[2,0,0]]
    face = [(0,1,2)]
    return verts, face

def normal_triangle():
    return np.array([[0.,0.,0.],[1.,0.,0.],[0.,1.,0.]]), [(0, 1, 2)]


CASES = [(
    'icosphere(0)', icosphere_0(),{
        'V' : 12, 'E' : 30, 'F' : 20, 'chi' : 2, 'components' : 1,
        'boundary_loops': 0, 'nonmanifold_edges' : 0,
        'nonmanifold_vertices' : [], 'is_manifold' : True,
        'is_closed' : True, 'is_oriented' : True, 'degenerate_faces' : []
    }),
    (
    '5X5 grid', grid_5(),{
            'V' : 36, 'E' : 60, 'F' : 25, 'chi' : 1, 'components' : 1,
            'boundary_loops': 1, 'nonmanifold_edges' : 0,
            'nonmanifold_vertices' : [], 'is_manifold' : True,
            'is_closed' : False, 'is_oriented' : True, 'degenerate_faces' : []
    }),

    (
    'two_spheres', two_spheres(),{
            'V' : 24, 'E' : 60, 'F' : 40, 'chi' : 4, 'components' : 2,
            'boundary_loops': 0, 'nonmanifold_edges' : 0,
            'nonmanifold_vertices' : [], 'is_manifold' : True,
            'is_closed' : True, 'is_oriented' : True, 'degenerate_faces' : []
        }),

    (
    'bow_tie', bowtie(),{
            'V' : 5, 'E' : 6, 'F' : 2, 'chi' : 1, 'components' : 1,
            'boundary_loops': 1, 'nonmanifold_edges' : 0,
            'nonmanifold_vertices' : [0], 'is_manifold' : False,
            'is_closed' : False, 'is_oriented' : True, 'degenerate_faces' : []
        }),
    (
    'three_on_edge', three_on_edge(),{
            'V' : 5, 'E' : 7, 'F' : 3, 'chi' : 1, 'components' : 1,
            'boundary_loops': 1, 'nonmanifold_edges' : 1,
            'nonmanifold_vertices' : [0, 1], 'is_manifold' : False,
            'is_closed' : False, 'is_oriented' : False, 'degenerate_faces' : []
        }),
    (
    'reverse_surface', reversed_face(),{
            'V' : 12, 'E' : 30, 'F' : 20, 'chi' : 2, 'components' : 1,
            'boundary_loops': 0, 'nonmanifold_edges' : 0,
            'nonmanifold_vertices' : [], 'is_manifold' : True,
            'is_closed' : True, 'is_oriented' : False, 'degenerate_faces' : []
        })
    ]

passed = 0
for name, (verts, faces), expected in CASES:
    d = mesh_stats_arrays(verts, faces)
    got = {k: d[k] for k in expected}
    if got == expected:
        print(f'{name}: PASS')
        passed += 1
    else:
        print(f'{name}: FAIL')
        for k in expected:
            if got[k] != expected[k]:
                print(f'    {k}: expected {expected[k]!r}, got {got[k]!r}')

def test_degenerate_face():
    cases = [
    ('repeat_vertex', degen_repeat_vertex(), [0]),
    ('degen_collinear', degen_collinear(),    [0]),
    ('normal_triangle', normal_triangle(),  []),
    ]
    passed = 0
    for name, (verts, faces), expected in cases:
        got = degenerate_faces(verts, faces)
        if got == expected:
            print(f'{name}: PASS')
            passed += 1
        else:
            print(f'{name}: FAIL  expected {expected!r}, got {got!r}')
    return passed, len(cases)

DP, DN = test_degenerate_face()
total_pass = passed + DP
total_all  = len(CASES) + DN
print(f'\n{total_pass} passed, {total_all - total_pass} failed')
sys.exit(0 if total_pass == total_all else 1)