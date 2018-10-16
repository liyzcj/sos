import numpy as np
import tsp

d = np.loadtxt("../map1.txt")
r = range(len(d))

dist = {(i, j): d[i][j] for i in r for j in r}
print(tsp.tsp(r, dist))
