import numpy as np
#随机生成10000*4的nparray
Z = np.random.random((10000,4))
#第二，三列改成5-50之间的随机数
Z[:,2] = np.random.uniform(5,50,10000)
Z[:,3] = np.random.uniform(5,50,10000)
print(Z)
#面积
arr = Z
area = arr[:,2]* arr[:,3]
print(area)
#坐标
Z[:,0] = np.random.uniform(0,1000,10000)
Z[:,1] = np.random.uniform(0,1000,10000)
#划分 10*10的筒
x_bin =  (Z[:,0]//100).astype(int)
y_bin =  (Z[:,1]//100).astype(int)
#划分100个街区，计算密度，输出带密度，格子坐标
def Cover_Ratio(Z):
    results = []
    for i in range(10):
        for j in range(10):
            mask = (x_bin == i) & (y_bin == j)
            total = area[mask].sum()
            ratio = total/10000
            results.append((ratio,i,j))
    return(results)
#高到低排序，取前5
results = Cover_Ratio(Z)
results.sort(reverse=True)
print(results[:5])
#建立shapely 10*10，用numpy，把街区ratio赋值进
grid = np.zeros((10,10))
for ratio,i,j in results:
    grid[i,j] = ratio
#plt输出图表
import matplotlib.pyplot as plt
plt.imshow(grid,cmap='OrRd')
plt.colorbar(label='Coverage Ratio')
plt.show()

