"""
Created on Tue Oct 16 05:03:48 2018

@author: liyanzhe
"""
import numpy as np
import matplotlib.pyplot as plt


class Ant:

    def __init__(self, nc):
        self.path = []
        self.length = 0
        self.visiting = 0
        self.allowed = list(range(nc))
        self.nc = nc

    def go_next(self, tau, eta, a, b):
        P = np.zeros(len(self.allowed))  # initial probability
        for k in range(len(self.allowed)):
            P[k] = (tau[self.visiting][self.allowed[k]] ** a) * \
                   (eta[self.visiting][self.allowed[k]] ** b)
        P = P / np.sum(P)
        # randomly choose next according probability
        Pcum = np.cumsum(P)
        _index = np.where(Pcum >= np.random.rand())
        to_visit = self.allowed[_index[0][0]]
        # add to path and remove from allowed
        self.path.append(to_visit)
        self.allowed.remove(to_visit)
        self.visiting = to_visit

    def compute_length(self, g):
        for step in range(self.nc - 1):
            self.length += g[int(self.path[step])][int(self.path[step + 1])]
        # length for the last step
        self.length += g[int(self.path[self.nc - 1])][int(self.path[0])]


class Aco:

    def __init__(self, K=100, iters=100, Q=200):

        self.K = K
        self.iters = iters
        self.Q = Q

    def solve(self, g, p):
        nc = np.size(g, axis=1)  # number of city
        eta = 1 / g  # heuristic factor = 1 / d
        tau = np.ones((nc, nc))  # initial matrix of pheromone

        best_path_iter = np.zeros((self.iters, nc))  # best path for every iter
        best_length_iter = np.inf * np.ones((self.iters, 1))  # best length for every iteration
        iter_avg_length = np.zeros((self.iters, 1))  # avg length for iteration

        for it in range(self.iters):
            ants = [Ant(nc) for _ in range(self.K)]  # initial ants
            for ant in ants:
                #                print(type(ant.path))
                ant.path.append(np.random.randint(nc))
                ant.visiting = ant.path[0]
                ant.allowed.remove(ant.visiting)

            for step in range(1, nc):
                for ant in ants:
                    ant.go_next(tau, eta, p[0], p[1])
            # add best path in last iteration to current one 
            if it >= 1:
                ants[0].path = best_path_iter[it - 1]

            # compute best length
            all_length = []
            for ant in ants:
                ant.compute_length(g)
                all_length.append(ant.length)

            # save best length and path
            for ant in ants:
                if ant.length == min(all_length):
                    best_length_iter[it] = ant.length
                    best_path_iter[it] = np.array(ant.path)
                    iter_avg_length[it] = np.mean(all_length)
                    break
            print("it = ", it, " best length = ", min(all_length))
            # update pheromone
            delta_tau = np.zeros((nc, nc))
            for ant in ants:
                for n in range(nc - 1):
                    delta_tau[int(ant.path[n])][int(ant.path[n + 1])] += self.Q / ant.length
                delta_tau[int(ant.path[nc - 1])][int(ant.path[1])] += self.Q / ant.length

            tau = (1 - p[2]) * tau + delta_tau
            # compute best solution global
        best_iter = np.where(best_length_iter == min(best_length_iter))
        best_length = best_length_iter[best_iter[0][0]]
        best_path = best_path_iter[best_iter[0][0]]

        # plot figure
        plt.plot(best_length_iter)
        plt.plot(iter_avg_length, 'r')
        plt.xlabel('iteration')
        plt.ylabel('length')
        plt.legend(['length', 'length avg'])
        plt.show()

        return best_length, best_path


if __name__ == "__main__":

    # length matrix
    g1 = np.loadtxt("map1.txt")
    g2 = np.loadtxt("map2.txt")
    g3 = np.loadtxt("map3.txt")
    print(g1.shape,g2.shape,g3.shape)
    # K = 50  # number of ant (equal number of cite)
    # iters = 100  # number of iteration
    # Q = 100  # Pheromone increase factor

    # alpha = 1  # importance of pheromone
    # beta = 2  # importance of heuristics
    # rho = 0.1  # Pheromone attenuation factor
    param = (1, 2, 0.1)
    """
    param: alpha, beta, rho
    """

    aco = Aco()
    solution = aco.solve(g1, param)
    print(solution)
