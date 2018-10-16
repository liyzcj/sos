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
        self.array = [[0] * (2 ** len(self.g)) for _ in range(len(self.g))]

    @staticmethod
    def transfer(sets):
        su = 0
        for s in sets:
            su = su + 2 ** s
        return su

    # main interface
    def tsp(self):
        s = self.start
        nc = len(self.g)
        cities = list(range(nc))  # initial list of city
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

        dis = min(distance)

        # next node, the nearest one
        next_one = unvisited[distance.index(dis)]

        c = self.transfer(unvisited)

        self.array[node][c] = next_one

        return dis


if __name__ == '__main__':
    d = np.loadtxt("../map1.txt")
    dp = Dp(d, 0)

    print(dp.tsp())

    M = dp.array
    lists = list(range(len(dp.g)))
    start = dp.start
    while len(lists) > 0:
        lists.pop(lists.index(start))
        m = dp.transfer(lists)
        next_node = dp.array[start][m]
        print(start, "--->", next_node)
        start = next_node
