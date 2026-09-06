#kriging
import os
import laspy
from pykrige import OrdinaryKriging
import numpy as np
import matplotlib.pyplot as plt

script_dir= os.path.dirname(__file__)
data_dir = os.path.join(script_dir,'..', 'data','C_37EN2.LAZ')

with laspy.open(data_dir) as reader:
    data0 = next(reader.chunk_iterator(1000000))
    #ground code
    ground = data0[data0.classification == 2]
    idx= np.random.choice(len(ground), 300, replace=False)
    #select xyz
    x = ground.x[idx]
    y = ground.y[idx]
    z = ground.z[idx]
    #kriging
    ok1 =OrdinaryKriging(x, y, z, variogram_model='spherical')
    #np build xs, ys
    xs = np.arange(x.min(),x.max(), 2)
    ys = np.arange(y.min(), y.max(), 2)
    z_krigm, sigma = ok1.execute('grid', xs, ys)

    print(f'X:{x.min():.1f}~{x.max():.1f}, Y:{y.min():.1f}~{y.max():.1f}')
    print(type(z_krigm))
    
    plt.imshow(z_krigm, cmap ='terrain')
    plt.show()
    plt.subplot()
    plt.imshow(sigma, cmap ='terrain')
    plt.show()
