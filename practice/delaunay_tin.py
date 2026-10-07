#delaunay_tin
import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial import Delaunay, Voronoi, voronoi_plot_2d
import os
script_dir = os.path.dirname(__file__)
out_dir = os.path.join(script_dir, '..', 'output')

rng = np.random.default_rng(8)
pts = rng.random((30,2))

tri = Delaunay(pts)

fig, ax = plt.subplots(figsize=(7,7))
ax.triplot(pts[:,0],pts[:,1],tri.simplices, color = 'steelblue', lw = 0.8)
ax.plot(pts[:,0],pts[:,1], 'o',color = 'crimson', ms = 4)
ax.set_aspect('equal'); ax.set_title(f'Delaunay TIN -{len(tri.simplices)} triangles')

vor = Voronoi(pts)
voronoi_plot_2d(vor, ax=ax, show_points = False, line_colors = 'orange',
                line_width = 0.6, line_alpha = 0.5)

os.makedirs(out_dir, exist_ok=True)
plt.savefig(os.path.join(out_dir, 'delaunay_tin.png'), dpi=200)
plt.show()