#LAZ practice
import laspy
import os
import numpy as np
import matplotlib.pyplot as plt 


script_dir = os.path.dirname(__file__)
data_dir = os.path.join(script_dir,'..','data','C_37EN2.LAZ')

#data0 = laspy.read(data_dir)

#data0_analyse = np.unique(data0.classification,return_counts = True)
#print(data0_analyse)

with laspy.open(data_dir) as reader:
    data0 = next(reader.chunk_iterator(10000))
    cls, cnt = np.unique(data0.classification,return_counts = True)
    print('\nfinal classification:')
    for c, n in zip(cls,cnt):
        print(f'class{c}:{n:,}')
    print(type(data0))
    print(f'bbox min: {reader.header.min}')
    print(f'bbox max: {reader.header.max}')

    x_min,y_min,_ = reader.header.min
    x_max,y_max,_ = reader.header.max

    x_range = x_max - x_min
    y_range = y_max - y_min
    cover_area = x_range * y_range
    print(f'cover_area:{cover_area:.2f}')

    n = 5000
    idx = np.random.choice(len(data0), n, replace=False)
    sample = data0[idx]

    fig, ax = plt.subplots(figsize=(10, 8), subplot_kw={'projection':'3d'})

    sc = ax.scatter(sample.x, sample.y, sample.z, c=sample.z ,cmap='terrain',s =1, alpha=0.8)
    ax.set_xlabel('X(RD)')
    ax.set_ylabel('Y(RD)')
    ax.set_zlabel('Z(m)')
    ax.set_title(f'AHN4 SAMPLE {n}')

    plt.colorbar(sc, label = 'Elevation(m)')
    plt.show()