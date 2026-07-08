#1
import numpy as np
#2
print(np.__version__)
np.show_config()
3#
Z = np.zeros(10)
print(Z)
#4
Z = np.zeros((10,10))
print(Z)
print("%d bytes" % (Z.size *Z.itemsize))
#5
#%run 'python -c "import numpy;numpy.info(numpy.add)"'
#6
Z = np.zeros(10)
Z[4] = 1
print(Z)
#7
Z = np.arange(10,50)
print(Z)
#8
Z = np.arange(10,50)
Y = Z[::-1]
print(Y)
#9
Z = np.arange(0,9).reshape(3,3)
Y = np.reshape(Z,(1,9))
print(Y)
#10
Z = np.nonzero([1,2,0,0,4,0])
print(Z)
#11
Z = np.eye(3)
print(Z)
#12
Z = np.random.random((3,3,3))
print(Z)
#13
Z = np.random.random((10,10))
Y = Z.min()
print(Y)
#14
Z = np.random.random(30)
m = Z.mean()
print(m)
#15
Z = np.ones((4,4))
Z[1:-1,1:-1] = 0
print(Z)
#16
Z = np.ones((5,5))
Z = np.pad(Z, pad_width=1, mode="constant",constant_values=0)
print(Z)
#18
Z = np.diag(1+np.arange(4),k=-1)
print(Z)
#19
Z = np.zeros((8,8),dtype=int)
Z[1::2,::2] = 1
Z[::2,1::2] = 1
print(Z)
#20
Z = np.arange(0,6*7*8).reshape(6,7,8)
Z = np.unravel_index(99,(6,7,8))
print(Z)
#21
