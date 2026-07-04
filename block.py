import numpy as np

Z = np.random.random((10000,4))
Z[:,2] = np.random.uniform(5,50,10000)
Z[:,3] = np.random.uniform(5,50,10000)
print(Z)

arr = Z
area = arr[:,2]* arr[:,3]
print(area)

Z[:,0] = np.random.uniform(0,1000,10000)
Z[:,1] = np.random.uniform(0,1000,10000)
x_bin =  (Z[:,0]//100).astype(int)
y_bin =  (Z[:,1]//100).astype(int)

def Cover_Ratio(Z):
    results = []
    for i in range(10):
        for j in range(10):
            mask = (x_bin == i) & (y_bin == j)
            total = area[mask].sum()
            ratio = total/10000
            results.append((ratio,i,j))
    return(results)

results = Cover_Ratio(Z)
results.sort(reverse=True)
print(results[:5])

grid = np.zeros((10,10))
for ratio,i,j in results:
    grid[i,j] = ratio

import matplotlib.pyplot as plt
plt.imshow(grid,cmap='OrRd')
plt.colorbar(label='Coverage Ratio')
plt.show()

