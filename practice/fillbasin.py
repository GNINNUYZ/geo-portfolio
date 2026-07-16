from pysheds.grid import Grid
import os
import matplotlib.pyplot as plt
import numpy as np
if not hasattr(np, 'in1d'):
    np.in1d = np.isin


script_path = os.path.dirname(__file__)
data_path = os.path.join(script_path,'..','dem.tif')
#open 
grid0 = Grid.from_raster(data_path)
dem = grid0.read_raster(data_path)

#fillbasin
dem_fill = grid0.fill_depressions(dem)
#waterflow
flow_dir = grid0.flowdir(dem_fill)
#watertogether
watertogether = grid0.accumulation(flow_dir)

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12,5))
ax1.imshow(flow_dir, cmap ='viridis')
ax1.set_title('Flow dirction')
ax2.imshow(watertogether, cmap = 'Blues')
ax2.set_title('Water together')
plt.show()

#find out
threshold = 50
x0, y0 = np.unravel_index(np.nanargmax(watertogether), watertogether.shape)[::-1]
x_snap, y_snap = grid0.snap_to_mask(watertogether > threshold, (x0, y0))

outsite = grid0.catchment(x=x_snap, y = y_snap, fdir=flow_dir, out_name='catchflow',xytype='index')

plt.imshow(outsite, cmap='Blues')
plt.show()