# 02 - Half-edge Engine

A hand-written half-edge data structure for 3D meshes, with no external geometry libraries.

## Pipeline

1. Parse OBJ vertices / faces
2. Build vertex, half-edge and face records
3. Link `twin`, `next`, `prev` pointers
4. Verify on `cube.obj`

## Files

- `halfedge.py`

## Run

```bash
python halfedge.py
```

## Test Data

- `../data/cube.obj`
