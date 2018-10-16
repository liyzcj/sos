"""
Created on Mon Oct 15 04:03:16 2018

@author: liyanzhe
"""
import numpy as np


# Dynamic programming for tsp
class Dp:
    def __init__(self, g, s):
        self.g = g  # the graph matrix
        self.start = s  # start node
        self.array = [[0] * (2 ** len(self.g)) for _ in range(len(self.g))]  # 记录处于x节点，未经历M个节点时，矩阵储存x的下一步是M中哪个节点

    @staticmethod
    def transfer(sets):
        su = 0
        for s in sets:
            su = su + 2 ** s
        return su

    # tsp总接口
    def tsp(self):
        s = self.start
        num = len(self.g)
        cities = list(range(num))  # initial list of city
        cities.pop(cities.index(s))  # unvisited
        node = s  # initial start node
        return self.solve(node, cities)

    def solve(self, node, unvisited):
        # recursion stop flat
        if len(unvisited) == 0:
            return self.g[node][self.start]
        distance = []

        # traversing unvisited
        for i in range(len(unvisited)):
            s_i = unvisited[i]
            copy = unvisited[:]
            copy.pop(i)  # remove visiting
            # recursive visiting
            distance.append(self.g[node][s_i] + self.solve(s_i, copy))

        d = min(distance)
        # next node, the nearest one
        next_one = unvisited[distance.index(d)]

        c = self.transfer(unvisited)

        self.array[node][c] = next_one
        return d


#
# D = [[-1, 10, 20, 30, 40, 50],
#     [12, -1, 18, 30, 25, 21],
#     [23, 19, -1, 5, 10, 15],
#     [34, 32, 4, -1, 8, 16],
#     [45, 27, 11, 10, -1, 18],
#     [56, 22, 16, 20, 12, -1]]

D = np.loadtxt("map1.txt")

dp = Dp(D, 0)
print(dp.tsp())
# 开始回溯
M = dp.array
lists = list(range(len(dp.g)))
start = dp.start
while len(lists) > 0:
    lists.pop(lists.index(start))
    m = dp.transfer(lists)
    next_node = dp.array[start][m]
    print(start, "--->", next_node)
    start = next_node
