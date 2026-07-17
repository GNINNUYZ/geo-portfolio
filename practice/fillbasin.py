from pysheds.grid import Grid
import os
import matplotlib
matplotlib.use("Qt5Agg")
import matplotlib.pyplot as plt

import numpy as np
if not hasattr(np, 'in1d'):
    np.in1d = np.isin


script_path = os.path.dirname(__file__)
data_path = os.path.join(script_path,'..', 'dem.tif')
#open 
grid0 = Grid.from_raster(data_path)
dem = grid0.read_raster(data_path)

#fillbasin
dem_fill = grid0.fill_depressions(dem)
dem_fill = grid0.resolve_flats(dem_fill)
#waterflow
flow_dir = grid0.flowdir(dem_fill)
#watertogether
watertogether = grid0.accumulation(flow_dir)

#outpoint
threshold = 50
x0, y0 = np.unravel_index(np.nanargmax(watertogether), watertogether.shape)[::-1]
x_snap, y_snap = grid0.snap_to_mask(watertogether > threshold, (x0, y0))
catch_big_streams = grid0.catchment(x=x_snap, y = y_snap, fdir=flow_dir, out_name='catchflow',xytype='coordinate')
#tunnel
tunnel0 = watertogether > threshold
plt.imsave('tunnel.png', tunnel0, cmap = 'Blues')
print('Saved tunnel.png')
#Save
plt.imsave('flow_dir.png', flow_dir, cmap='viridis')
print('Saved flow_dir.png')
plt.imsave('water_together.png', watertogether, cmap='Blues')
print('Saved water_together.png')
plt.imsave('streams.png', catch_big_streams, cmap='Blues')
print('Saved streams.png')