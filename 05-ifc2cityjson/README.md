# 05 - IFC → CityJSON

Converts an IFC building model (BIM) into a CityJSON 3D city model with semantic surfaces.

## Pipeline

1. Open IFC with IfcOpenShell
2. Extract shell geometry in world coordinates
3. Map IFC semantics: Wall / Slab / Window / Door → CityJSON surface types
4. Assemble CityJSON v1.1 (vertices + boundaries + semantics)

## Files

- `coordinate_change.py` — converter
- `output.city.json` — output CityJSON

## Run

```bash
python coordinate_change.py
```

## Output

`output.city.json` — can be inspected at [ninja.cityjson.org](https://ninja.cityjson.org)

## Dependencies

- `ifcopenshell`
- `cjio`
