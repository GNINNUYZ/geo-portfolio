
CREATE EXTENSION postgis;

SELECT PostGIS_Version();

CREATE TABLE buildings (
    id          TEXT PRIMARY KEY,
    name        TEXT,
    geom3d      GEOMETRY(POLYHEDRALSURFACEZ, 28992),
    attributes  JSONB DEFAULT '{}'::jsonb,
    components  JSONB DEFAULT '[]'::jsonb,
    bbox3d      GEOMETRY(POLYHEDRALSURFACEZ, 28992)
);

CREATE INDEX idx_buildings_geom3d ON buildings USING GIST (geom3d);
CREATE INDEX idx_buildings_attrs  ON buildings USING GIN (attributes);

