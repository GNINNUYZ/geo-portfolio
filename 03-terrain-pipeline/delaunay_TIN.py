#delaunay TIN
from scipy.spatial import Delaunay
import laspy
import numpy as np
import os
import matplotlib.pyplot as plt
from scipy.interpolate import LinearNDInterpolator
import rasterio
from rasterio.transform import from_origin

#文件
scr_path = os.path.dirname(__file__)
data_path = os.path.join(scr_path,'..','data', 'delft_50_crop.laz')

#laspy open
with laspy.open(data_path) as reader:
        data0 = reader.read()

    #取point,random down sample
        ground0 = data0[data0.classification == 2]
        x0_min, x0_max = ground0.x.min(), ground0.x.max()
        y0_min, y0_max = ground0.y.min(), ground0.y.max()
        corners = [(x0_min, y0_min),(x0_min, y0_max),(x0_max, y0_min),(x0_max, y0_max)]

        idx = np.random.choice(len(ground0), 20000, replace=False)
        for cx, cy in corners:
              d = (ground0.x - cx)**2 + (ground0.y - cy)**2
              unique = np.argmin(d)
              idx = np.append(idx, unique)
        idx= np.unique(idx)
        ground = ground0[idx]
        pts = np.column_stack([ground.x[:], ground.y[:]])
        #delaunay
        tri =Delaunay(pts) 
    #insert TIN point

        xs = np.arange(x0_min + 0.5, x0_max, 1)
        ys = np.arange(y0_min + 0.5, y0_max, 1)
        gx, gy = np.meshgrid(xs, ys)
        xi = gx.ravel()
        yi = gy.ravel()
        grid_pts = np.column_stack((xi,yi))

        simplex = tri.find_simplex(grid_pts)
        valid = simplex >= 0
        nan = simplex < 0
        trans_matrix = tri.transform[simplex[valid]]

        pts_3d = np.column_stack([ground.x[:], ground.y[:], ground.z[:]])
        
        tri_vertix = tri.simplices[simplex[valid]]
        interp = LinearNDInterpolator(pts, ground.z[:])
        rows, cols = gx.shape
        dem = interp(xi,yi).reshape(rows,cols)
        
        #rasterio export
        transform = from_origin(x0_min, y0_max, 1, 1)
        with rasterio.open(os.path.join(scr_path, 'dem.tif'), 'w', driver ='GTiff',
                        height=rows,width=cols,count=1,
                        dtype='float32', crs='EPSG:28992',
                        transform=transform) as dst:
            dst.write(dem.astype('float32'), 1)
        plt.imsave('dem_preview.png', np.nan_to_num(dem, nan=np.nanmin(dem)), cmap ='terrain')


#plt
fig, ax = plt.subplots(figsize =(10,8), subplot_kw={'projection':'3d'})
#triangular
sc = ax.plot_trisurf(ground.x[:], ground.y[:], ground.z[:], triangles=tri.simplices, cmap ='terrain',  alpha = 0.8)
fig.savefig(os.path.join(scr_path,'3d_dem_preview.png'))
plt.show()


plt.subplot()
plt.imshow(dem,cmap = 'terrain',origin='upper')
plt.show()