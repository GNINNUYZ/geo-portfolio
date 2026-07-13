#delaunay TIN
from scipy.spatial import Delaunay
import laspy
import numpy as np
import os
import matplotlib.pyplot as plt
from scipy.interpolate import LinearNDInterpolator

#文件
scr_path = os.path.dirname(__file__)
data_path = os.path.join(scr_path,'..','data', 'C_37EN2.LAZ')

#laspy open
with laspy.open(data_path) as reader:
    #prev 10000 point
    for chunk in reader.chunk_iterator(1000000):
        data0 = chunk
        break
    #取point,random down sample
    n = 5000
    ground0 = data0[data0.classification == 2]
    idx = np.random.choice(len(ground0), n, replace = False)
    ground = ground0[idx]
    pts = np.column_stack([ground.x[:500], ground.y[:500]])
    #delaunay
    tri =Delaunay(pts)
#insert TIN point
    x_min, x_max = ground.x.min(), ground.x.max()
    y_min, y_max = ground.y.min(), ground.y.max()
    xs = np.arange(x_min, x_max, 1)
    ys = np.arange(y_min, y_max, 1)
    gx, gy = np.meshgrid(xs, ys)
    xi = gx.ravel()
    yi = gy.ravel()
    grid_pts = np.column_stack((xi,yi))

    simplex = tri.find_simplex(grid_pts)
    valid = simplex >= 0
    nan = simplex < 0
    trans_matrix = tri.transform[simplex[valid]]

    pts_3d = np.column_stack([ground.x[:500], ground.y[:500], ground.z[:500]])
    
    tri_vertix = tri.simplices[simplex[valid]]
    interp = LinearNDInterpolator(pts, ground.z[:500])
    rows, cols = gx.shape
    dem = interp(xi,yi).reshape(rows,cols)

    


#plt
fig, ax = plt.subplots(figsize =(10,8), subplot_kw={'projection':'3d'})
#triangular
sc = ax.plot_trisurf(ground.x[:500], ground.y[:500], ground.z[:500], triangles=tri.simplices, cmap ='terrain',  alpha = 0.8)
plt.show()

plt.subplot()
plt.imshow(dem,cmap = 'terrain',origin='upper')
plt.show()
    



def tin_insertpoint(tri, points_3d, xi, yi):
     simplex = tri.find_simplex(np.column_stack[xi, yi])

