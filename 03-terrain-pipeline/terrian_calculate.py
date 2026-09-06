#terrian_calculate
import os
import rasterio
import numpy as np
import matplotlib.pyplot as plt

script_dir = os.path.dirname(__file__)
data_dir = os.path.join(script_dir, 'dem.tif')

with rasterio.open(data_dir) as src:
    dem = src.read(1)
    print(type(dem))
    #print(np.dtype(np.gradient(dem)))
    #导数
    dz_dy,dz_dx = np.gradient(dem)
    #print(dz_dy)
    #slope
    slope = np.sqrt(dz_dx**2 +dz_dy**2)
    slope_degree = np.degrees(np.arctan(slope))
    #aspect
    aspect = np.degrees(np.arctan2(-dz_dx, -dz_dy))
    #shade
    sun_angle = np.radians(45)
    sun_asp = np.radians(315)
    slope_rad = np.arctan(np.sqrt(dz_dx**2 +dz_dy**2))
    aspect_rad = np.arctan2(-dz_dx, -dz_dy)
    hillshade = 255 * (np.cos(sun_asp) *np.cos(slope_rad) + np.sin(sun_asp)*np.sin(slope_rad)*(np.cos(sun_asp - aspect_rad)))
    hillshade = np.nan_to_num(hillshade, nan=0).astype('uint8')
    plt.imsave(os.path.join(script_dir,'hillshade.png'), hillshade, cmap = 'grey')