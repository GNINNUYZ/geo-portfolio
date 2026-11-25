# 02 — Half-edge Engine

A hand-written half-edge data structure, a mesh diagnostic tool, a mesh-distance
function, an edge-flip operator, and a Marching Cubes isosurface extractor.
**No external geometry libraries** — no Open3D, no PCL, no trimesh, no scikit-image.
Every algorithm is written from the definitions and checked numerically.

## Files

| File | What it is |
|---|---|
| `halfedge.py` | half-edge structure: `twin` / `next` / `prev`, 2-manifold checks, vertex traversal, OBJ read/write |
| `icosphere.py` | icosphere generator with recursive subdivision (`sub = 0..4`) |
| `mesh_stats.py` | 16-field mesh diagnostic (topology + manifoldness + degeneracy) |
| `hausdorff.py` | three distance layers: point→surface, point-set→mesh, mesh→mesh (Hausdorff + a Lipschitz upper bound) |
| `edge_flip.py` | flip one interior edge of a triangle mesh by rewiring pointers only |
| `mc_table.py` | Marching Cubes triangle lookup table (256 rows, pure data) |
| `marching_cubes.py` | full-grid Marching Cubes: scalar field + iso → `(verts, faces)` |
| `to_cloudcompare.py` | export an icosphere to `.obj` for visual inspection |
| `test_mesh_stats.py` | 9 test cases |
| `test_hausdorff.py` | 22 assertions |
| `test_edge_flip.py` | 11 assertions |
| `test_marching_cubes.py` | 22 assertions |

## Verify

```bash
python test_mesh_stats.py
python test_hausdorff.py
python test_edge_flip.py
python test_marching_cubes.py
```

Expected:

```
9 passed, 0 failed
22 passed, 0 failed
11 passed, 0 failed
22 passed, 0 failed
```

**64 assertions total.** Exit code is `0` when everything passes and `1` otherwise, so
these can be used in CI. On failure each script prints the case name, the field name,
the expected value and the actual value — not just `FAIL`.

Requires only Python 3 + NumPy.

---

# Part 1 — mesh diagnostics (`mesh_stats.py`)

## What the test cases cover

| Case | Why it exists |
|---|---|
| `icosphere(0)` | closed sphere, `V/E/F = 12/30/20`, `chi = 2` |
| `5X5 grid` | quad mesh with boundary — **20 boundary edges forming exactly 1 loop** (counting components of the boundary graph, not boundary edges, is the part that is easy to get wrong) |
| `two_spheres` | `components = 2` and `chi = 4 = 2 + 2` (per-component, not a single number) |
| `bow_tie` | two faces touching at one vertex only: **no non-manifold edge at all**, yet one non-manifold vertex |
| `three_on_edge` | three faces on one edge: non-manifold edge, 2 non-manifold vertices, inconsistent orientation — one case exercising three independent checks |
| `reverse_surface` | one face flipped: **only `is_oriented` changes**, the other 11 fields are identical to `icosphere(0)` |
| `repeat_vertex` | face with a repeated vertex index |
| `degen_collinear` | three collinear points: Newell area is exactly 0 |
| `normal_triangle` | reverse case — a valid triangle must **not** be flagged |

Design rule: each invalid mesh changes exactly one field and holds the rest fixed, so a
failing assertion points at one piece of logic. `reverse_surface` is the reference
example — 11 of 12 fields are unchanged.

## The 16 fields

| Field | Meaning |
|---|---|
| `V` `E` `F` | vertex / undirected edge / face count |
| `chi` | Euler characteristic `V - E + F` |
| `components` | connected components of the vertex graph |
| `chi_per_component` | `chi` evaluated per component, so a disjoint mesh reads as a list, not a sum |
| `boundary_edges` | edges used by exactly one face |
| `interior_edges` | edges used by exactly two faces |
| `nonmanifold_edges` | edges used by three or more faces |
| `boundary_loops` | connected components of the **boundary-edge subgraph** |
| `bad_boundary_vertices` | vertices whose number of boundary edges is neither 0 nor 2 |
| `nonmanifold_vertices` | vertex indices whose link is not a single fan |
| `degenerate_faces` | face indices with a repeated vertex or near-zero Newell area |
| `is_manifold` | no non-manifold edge **and** no non-manifold vertex |
| `is_closed` | no boundary edge |
| `is_oriented` | no directed edge traversed twice in the same direction |

`boundary_edges + interior_edges + nonmanifold_edges == E` always holds — every edge
falls in exactly one of the three classes.

## Implementation notes

**Non-manifold edges vs non-manifold vertices.** An edge is non-manifold when it is
shared by 3+ faces; a vertex is non-manifold when the faces around it do not form a
single fan. These are independent: `bow_tie` has zero non-manifold edges but one
non-manifold vertex, so checking edges alone is not enough.

**Link criterion for vertices.** For vertex `v`, each incident face contributes one
edge between its two neighbours around `v`. The fan is a single piece iff that link
graph is connected, so the check is (a) number of connected components of the link
graph > 1, or (b) some neighbour has link-graph degree > 2. `v` itself is deliberately
**not** a node of the link graph — including it would connect everything and the test
would never fire.

**Degenerate faces use Newell's formula.** `nrm = Σ cross(p[k], p[(k+1) % m])` and
`area = 0.5 * ‖nrm‖`. This works for triangles and quads alike; the common
`cross(b - a, c - a)` form only holds for triangles. The threshold is relative to the
bounding-box diagonal (`1e-12 * ext²`), not a fixed absolute value.

**Orientation uses directed edges without normalisation.** If two adjacent faces
traverse their shared edge in the same direction, that directed edge is counted twice.
If they traverse it in opposite directions, each direction is counted once. So
`is_oriented` is falsified as soon as any directed edge count reaches 2 — the direction
is the signal, which is why it must not be normalised away with `min/max`.

## Verification numbers

| Mesh | `V` | `E` | `F` | `chi` | `components` | `boundary_loops` | `nonmanifold_edges` | `nonmanifold_vertices` |
|---|---|---|---|---|---|---|---|---|
| `icosphere(0)` | 12 | 30 | 20 | 2 | 1 | 0 | 0 | `[]` |
| `icosphere(2)` | 162 | 480 | 320 | 2 | 1 | 0 | 0 | `[]` |
| `5X5 grid` | 36 | 60 | 25 | 1 | 1 | 1 | 0 | `[]` |
| `two_spheres` | 24 | 60 | 40 | 4 | 2 | 0 | 0 | `[]` |
| `bow_tie` | 5 | 6 | 2 | 1 | 1 | 1 | **0** | **[0]** |
| `three_on_edge` | 5 | 7 | 3 | 1 | 1 | 1 | **1** | **[0, 1]** |

`icosphere(sub)` for `sub = 0..4`:

| `sub` | 0 | 1 | 2 | 3 | 4 |
|---|---|---|---|---|---|
| `V` | 12 | 42 | 162 | 642 | 2562 |
| `F` | 20 | 80 | 320 | 1280 | 5120 |

Every level has `chi = 2` and no boundary edges. The vertex-degree distribution is
`{5: 12, 6: V - 12}` — the 12 vertices of the original icosahedron keep degree 5, which
is the discrete form of "curvature is concentrated at 12 points" (Gauss–Bonnet:
`12 × 2π/6 = 4π = 2πχ`).

---

# Part 2 — mesh distance (`hausdorff.py`)

Three layers, because each one answers a different question:

| Function | Question |
|---|---|
| `p_dis2surf(pts, srf)` | distance from a point set to one triangle, point-to-point (no projection) |
| `p_dis2mesh(pts, mesh)` | minimum over all triangles → one scalar |
| `hausdorff(v1, m1, v2, m2)` | five values: `d1`, `d2`, `h1max`, `h2max`, `H_upper` |

## Why there is an upper bound, not the exact value

The exact Hausdorff distance between two triangle meshes needs the distance from a
**surface** to a **surface**, not from a point set. Sampling vertices only gives a lower
bound. The `H_upper` value uses the standard Lipschitz bound:

```
H_upper = max( d1 + R1,  d2 + R2 )
```

where `R1` is the longest edge of the source mesh — the largest distance from any point
of a triangle to its nearest vertex. So `H_upper` is a **guaranteed** upper bound on the
true Hausdorff distance, and the vertex-sampled `h1max`/`h2max` are lower bounds.

**All five values are asserted**, and the tests include the cases where the bound is
tight (nested cubes) and where it is loose.

## Why `l_max` needed `np.append` and not `+`

Computing the longest edge means, for each vertex, looking at the edge to its
**next** vertex, including the wrap-around pair `(n-1, 0)`. The natural attempt

```python
l1[1:] + l1[0]        #  scalar addition of the first element
```

silently drops that wrap-around pair. The bug only shows on a sliver triangle
`((0,0,0), (0.1,0,0), (10,0,0))`, where the answer should be `10.0` but comes out `9.9`.
Fixed with `np.append(l1[1:], l1[0])`.

## Why every comparison is `abs(got - expected) < tol`

A one-sided `got - expected <= 1e-6` passes when `got` is **far smaller** than expected.
Every assertion in `test_hausdorff.py` uses the absolute value, because the whole point
of the module is that a too-small answer is as wrong as a too-large one.

---

# Part 3 — edge flip (`edge_flip.py`)

`flip` rewires **16 pointer assignments** and creates **no new object**:

```
E = 12 assignments (6 next + 6 prev)   +   2 origin   +   2 face
```

So `V`, `E`, `F` cannot change — not because of careful bookkeeping, but because no
vertex, face or half-edge object is created or destroyed. That is the whole design:

| Before | After | Action |
|---|---|---|
| `a→b` | `a→b` | unchanged |
| `b→c`  (the diagonal) | `d→a` | reused, `origin` changed |
| `c→a` | `c→a` | **changes face** |
| `b→d` | `b→d` | **changes face** |
| `d→c` | `d→c` | unchanged |
| `c→b`  (the diagonal) | `a→d` | reused, `origin` changed |

Because the two diagonal half-edges are **reused**, their `twin` pairing survives
untouched, and the four boundary half-edges keep the `origin` and `face` they already
had. The only new information is which pointer points where.

## How the flip finds the right edge

The 12 half-edges are extracted from `he` alone, so no global search is needed:

```
he    = b→c          (one half of the interior edge)
he2   = he.twin      = c→b
h_ab  = he.prev      = a→b
h_ca  = he.next      = c→a
h_bd  = he2.next     = b→d
h_dc  = he2.prev     = d→c
a     = h_ab.origin
d     = h_dc.origin
```

`prev` existing is what makes this short: `he.prev.origin` is already `a`.

## Verification

The test asserts, after one flip:

| Check | Why |
|---|---|
| `V`, `E`, `F` unchanged | structural invariant (not evidence — see below) |
| edge-set difference is exactly `{(a,d)}` added and `{(b,c)}` removed | the only real evidence |
| `h.twin.twin is h` for all half-edges | pairing survived the reuse |
| `f.halfedge.next.next.next is f.halfedge` | the two cycles are still triangles |
| `f.halfedge.face is f` for all faces | `Face.halfedge` was re-pointed where needed |
| `boundary_edges() == 0` | closure preserved |

**`V/E/F` alone proves nothing** — the counts are identical before and after a
correct flip, and also identical after a wrong one. Only the edge **set** and the
structural checks distinguish them.

## Why only one flip

`flip` deliberately stops after the first flip. Flipping repeatedly while iterating the
same half-edge list cancels itself out:

```
6 face diagonals × 2 half-edges = 12 half-edges
→  flipping N of them gives |net change| = 0 for even N, 1 for odd N
→  never 6
```

Measured: `count = 1..12` gives net edge changes `1,0,1,0,1,0,1,0,1,0,1,0`. So
"flip six edges" is not a matter of picking the right count — it needs either an
iteration over **faces** (each face once) or a re-scan per flip. Both are needed for
Delaunay refinement, and neither is in scope here.

---

# Part 4 — Marching Cubes (`marching_cubes.py` + `mc_table.py`)

## Corner and edge numbering

Both must match `mc_table.py` exactly, because the lookup table is indexed by them.

```
corner   0=(0,0,0)  1=(1,0,0)  2=(1,1,0)  3=(0,1,0)
         4=(0,0,1)  5=(1,0,1)  6=(1,1,1)  7=(0,1,1)

edge     0:0-1   1:1-2   2:2-3   3:3-0      bottom ring
         4:4-5   5:5-6   6:6-7   7:7-4      top ring
         8:0-4   9:1-5  10:2-6  11:3-7      four verticals
```

This is **not** binary order (`x + 2y + 4z`); it is "walk the bottom face
counter-clockwise, then the top face". The difference is that corners `2` and `3` swap,
and so do `6` and `7`. Getting this wrong is silent: the isosurface is still extracted,
just at the wrong corner.

## The lookup table

`mc_table.py` holds 256 rows of 16 integers. Each group of three is one triangle
(three **edge numbers**); `-1` terminates. At most five triangles per cell, hence 15
numbers plus one sentinel.

It was validated against five invariants before use:

```
TRI_TABLE[0]     == all -1                 (nothing inside)
TRI_TABLE[255]   == all -1                 (everything inside)
TRI_TABLE[1][:3] == (0, 8, 3)
TRI_TABLE[2][:3] == (0, 1, 9)
every row has a multiple of 3 non-negative entries
```

The strongest check is the per-corner one: for each `k`, `triangles_of(2**k)` must
return exactly one triangle whose edge set equals the three edges incident to corner
`k`. That validates the corner↔edge correspondence, which is the part most likely to be
transcribed wrong.

## Vertex de-duplication

Adjacent cells share a face, so the same isosurface point gets computed by both. The
duplicate coordinates are **bit-identical** (same lattice points, same `t`, same
operation order), but they are two different array objects, so `build_from_arrays` sees
two vertices and the edge between them becomes a boundary edge — the mesh is no longer
closed.

The fix is to key on **which lattice edge** the point lies on, not on its coordinates:

```
edge number  →  EDGES[edge]  →  two corner numbers
             →  CORNERS[corner]  →  two offsets
             →  + cell index  →  two integer lattice points
             →  key = (min(p, q), max(p, q))            ← sorted
```

Sorting matters: cell A sees the shared edge from one end, cell B from the other.
Without sorting the two keys differ and nothing is merged.

## Results on a sphere

`f(x) = ‖x‖ − 1`, `iso = 0`, lattice `linspace(-1.5, 1.5, n)³`.

| `n` | verts | faces | radius range | area | vs `4π = 12.5664` | `chi` | boundary |
|---|---|---|---|---|---|---|---|
| 17 | 534 | 1064 | 0.9959 .. 1.0000 | 12.4271 | −1.11 % | 2 | 0 |
| 33 | 2142 | 4280 | 0.9990 .. 1.0000 | 12.5316 | −0.28 % | 2 | 0 |

Both area and radius error drop by ≈ 4× when `h` halves — **second-order convergence**,
which is what linear interpolation on the lattice edges predicts. That convergence rate,
not the absolute error, is the evidence the implementation is right: a wrong constant
factor would still land near 4π at one resolution, but would not converge at `O(h²)`.

Without de-duplication `n = 17` gives 3192 vertices; `3192 / 534 = 5.98 ≈ 6`, matching
the six edges incident to an interior lattice point.

## Why `V/E/F` alone would have missed a real bug

Before the world-coordinate fix, the output was in **index space**: vertex radii were
17–38 instead of ≈ 1, and the area was 14× too large. Yet `chi = 2`, `boundary = 0` and
`twin` pairing were all correct, because those three only look at connectivity, never at
coordinates. Only area and distance-to-analytic-sphere caught it.

So the two groups of checks are complementary:

```
chi / boundary / twin      verify topology
area / Hausdorff           verify geometry
```

## Implementation notes

**`meshgrid(..., indexing='ij')` and axis naming.** With `indexing='ij'`, the k-th
returned array varies along the k-th axis. Since `data.shape = (nz, ny, nx)`, axis 0 is
`z`, so the first returned array must be named `dz`. Naming it `X` is harmless for a
sphere (symmetric) but transposes an ellipsoid — volume stays the same, orientation
rotates 90°, and nothing reports an error. It also breaks anisotropic voxel spacing
(`L3-2`), where each axis has a different spacing.

**Loop variables leak.** After `for (cx, cy, cz) in CORNERS:` the three names still hold
`CORNERS[7]`. Reusing them inside a later loop does not raise — it silently computes
wrong keys.

---

## Known limitations

- **Marching Cubes does not handle the ambiguous cases.** Cells with four or more
  corners inside can be triangulated in more than one topologically valid way; the
  standard table picks one. On noisy real data this can change connectivity. Relevant
  from `L3` onwards.
- **No adaptive octree, no parallelism.** The full grid is scanned cell by cell in pure
  Python.
- **Edge flip supports one flip per call.** See Part 3.
- **`Face.halfedge` is not maintained across multiple flips.** Flipping six diagonals in
  a row leaves three faces pointing at a half-edge that now belongs to a different face.
  Only relevant for repeated flips (Delaunay refinement), not for a single flip.
- **`hausdorff` samples vertices, not surfaces.** `H_upper` is a bound, not the exact
  value.
- Half-edge construction is single-threaded and pure Python — fine up to ~10⁵ faces.

## Visual inspection

`to_cloudcompare.py` exports a mesh to `.obj` so it can be dropped into CloudCompare
(which is a viewer, not a solver):

```bash
python to_cloudcompare.py
```

This is worth doing for at least one mesh per module, because a number that "passes" can
still be the wrong shape. Two failures that survived dozens of numeric assertions and
were only visible as images were a 6-of-12 reversed winding in the cube fixture and the
index-space coordinates above.
