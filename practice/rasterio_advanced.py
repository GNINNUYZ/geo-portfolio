#rasterio advanced
import os
import rasterio
from rasterio.enums import Resampling
import matplotlib.pyplot as plt

script_dir = os.path.dirname(__file__)
data_dir = os.path.join(script_dir,'..','01-urban-density','data','ahn4_dtm_amsterdam.tif')

upscale_factor = 0.1
data1 = rasterio.open(data_dir)
#band2 = rasterio.read(data1,masked = True)

band1 = data1.read(1,
    out_shape = (
        data1.count,
        int(data1.height * upscale_factor),
        int(data1.width * upscale_factor)
    ),
    resampling = Resampling.bilinear
)

plt.imshow(band1, cmap = 'terrain')
plt.show()

from rasterio import warp
src = data1.read(1, masked = True)
import numpy as np
dst_transform, dst_width, dst_height = warp.calculate_default_transform(
    data1.crs, 'EPSG:4326', data1.width, data1.height, *data1.bounds
)
output_array = np.empty((dst_height, dst_width), dtype=data1.dtypes[0])

band2,_ = warp.reproject(source=src,
               destination=output_array,
               src_transform = data1.transform,
               src_crs=data1.crs,
               dst_transform=dst_transform,
               dst_crs='EPSG:4326',
               resampling = Resampling.bilinear
               )

plt.figure()
plt.imshow(band2, cmap = 'terrain')
plt.colorbar(label = 'Elevation(m)')
plt.show()