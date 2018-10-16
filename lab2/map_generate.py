import numpy as np

map3 = np.random.rand(11, 11) * 100
np.fill_diagonal(map3, np.finfo(float).eps)
print(map3)
np.savetxt("map3.txt", map3)