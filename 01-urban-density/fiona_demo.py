import fiona
import os

script_dir = os.path.dirname(__file__)
buildings_dir = os.path.join(script_dir,'..','data','amsterdam_buildings.json')
blocks_dir = os.path.join(script_dir,'..','data','amsterdam_wijken.json')

arch1 = fiona.open(buildings_dir)
block1 = fiona.open(blocks_dir)

print(arch1.driver)
print(arch1.crs)
print(arch1.schema)
print(arch1.bounds)

for i in arch1:
    props = i['properties']
    print(props['bouwjaar'])


output_path = os.path.join(script_dir,'..','data','new out_schema.json')

out_schema = {
    'geometry':block1.schema['geometry'],
    'properties':{'wijkcode':'str','wijknaam':'str'}
}

with fiona.open(output_path, 'w', driver='GeoJSON',
                crs=block1.crs,schema=out_schema) as dst:
    for feature in block1:
        new = {
            'geometry': feature['geometry'],
            'properties':{
                'wijkcode':feature['properties']['wijkcode'],
                'wijknaam':feature['properties']['wijknaam']
            }
        }
        dst.write(new)

