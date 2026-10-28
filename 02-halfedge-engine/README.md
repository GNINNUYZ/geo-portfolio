# 02 — Half-edge Engine

A hand-written half-edge data structure and mesh diagnostic tool for 3D meshes.
**No external geometry libraries** — no Open3D, no PCL, no trimesh. Everything is
written from the definitions and checked numerically.

## Files

| File | What it is |
|---|---|
| `halfedge.py` | half-edge structure: `twin` / `next` / `prev`, 2-manifold checks, vertex traversal |
| `icosphere.py` | icosphere generator with recursive subdivision (`sub = 0..4`) |
| `mesh_stats.py` | 16-field mesh diagnostic (topology + manifoldness + degeneracy) |
| `test_mesh_stats.py` | 9 test cases, prints per-case results, sets exit code |

## Verify

```bash
python test_mesh_stats.py
```

Expected output:

```
icosphere(0): PASS
5X5 grid: PASS
two_spheres: PASS
bow_tie: PASS
three_on_edge: PASS
reverse_surface: PASS
repeat_vertex: PASS
degen_collinear: PASS
normal_triangle: PASS

9 passed, 0 failed
```

Exit code is `0` when everything passes and `1` otherwise, so the script can be used
in CI. On failure it prints the case name, the field name, the expected value and the
actual value — not just `FAIL`.

Requires only Python 3 + NumPy.

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

Reproduce these by running the script; the assertions are the expected values.

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

## Run the half-edge engine separately

```bash
python halfedge.py
```

Verifies `twin` pairing, boundary edges and per-face orientation on `../data/cube.obj`
(`V/F/H = 8/6/24`).

## Known limitations

- No OBJ writer; input is arrays or OBJ read only.
- `degenerate_faces` uses an area threshold, so very thin but valid triangles in dense
  scans can in principle be flagged; the `1e-12` factor is deliberately loose.
- Half-edge construction is single-threaded and pure Python — fine up to ~10⁵ faces,
  not intended for large meshes.
- Test data in `../data/cube.obj`; everything else is generated procedurally.
