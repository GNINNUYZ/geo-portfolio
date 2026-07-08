import rasterio
import os
import matplotlib.pyplot as plt

script_dir = os.path.dirname(__file__)
dataset = rasterio.open(os.path.join(script_dir, '..', '01-urban-density','data', 'ahn4_dtm_amsterdam.tif'))

print(dataset.name)
print(dataset.mode)
print(dataset.width)
print(dataset.height)
print(dataset.crs)
print(dataset.count)
print(dataset.dtypes)
print(dataset.nodata)

band = dataset.read(1, masked = True)


transform = dataset.transform
col = dataset.width // 2
row = dataset.height // 2
x, y = dataset.xy(row, col)
row, col = dataset.index(x, y)

window = rasterio.windows.Window(col,row,200,200)
window_data = dataset.read(1, window=window)

#
plt.figure()
plt.hist(band.compressed(), bins=50)
plt.show()

plt.figure()
plt.imshow(band, cmap = 'terrain')
plt.colorbar(label = 'Elevation(m)')
plt.show()



#x,y = dataset.transform * (col,row)
#row, col = rasterio.transform.rowcol(dataset.transform, x, y)

