"""
Cat swarm Optimization

author: @ Liyanzhe, 2018.12.10
"""

import numpy as np
from random import choice, randint, random

class Cso:

    """
    Cat Swarm Optimization
    """
    def __init__(self, n, function, lb, ub, dimension, iteration, mr=10, smp=2,
                 spc=False, cdc=1, srd=0.1, w=0.1, c=1.05, csi=0.6):

        self.__Positions = []
        self.__Gbest = []

        # Initial Cat Agents position and velocity
        self.__agents = np.random.uniform(lb, ub, (n, dimension))
        velocity = np.zeros((n, dimension))
        self._points(self.__agents)
        # compute Pbest for each agent
        fitx = np.array([function(x) for x in self.__agents])
        Pbest = self.__agents[fitx.argmin()]

        Gbest = Pbest
        self.Gbest_fit = fitx.min()

        flag = self.__set_flag(n, mr)

        # spc label
        if spc:
            sm = smp-1
        else:
            sm = smp

        for t in range(iteration):

            for i in range(n):
                print("==========================ITER {}: Particle {}============================".format(t, i))
                if flag[i] == 0:
                    
                    if spc:

                        cop = self.__change_copy([self.__agents[i]], cdc, srd)[
                            0]
                        tmp = [self.__agents[i] for j in range(sm)]
                        tmp.append(cop)
                        copycat = np.array(tmp)

                    else:
                        copycat = np.array([self.__agents[i] for j in range(sm)])
                    copycat = self.__change_copy(copycat, cdc, srd)

                    if copycat.all() == np.array(
                            [copycat[0] for j in range(sm)]).all():
                        P = np.array([1 for j in range(len(copycat))])
                        ccc = 0

                    else:
                        ccc = 1
                        copy_fit = [function(j) for j in copycat]
                        fb = min(copy_fit)
                        fmax = max(copy_fit)
                        fmin = min(copy_fit)
                        P = np.array(
                            [abs(copy_fit[j] - fb) / (fmax - fmin) for j in
                             copycat])
                    self.__agents[i] = copycat[P.argmax()]
                    if ccc:
                        fitx[i] = copy_fit[P.argmax()]
                else:

                    ww = w + (iteration - t) / (2 * iteration)
                    cc = c - (iteration - t) / (2 * iteration)
                    r = random()
                    velocity[i] = ww * np.array(velocity[i]) + r * cc * (
                        np.array(Pbest) - np.array(self.__agents[i]))
                    vinf, cinf = self.__get_inf(i, velocity, self.__agents,
                                                csi)
                    self.__agents[i] = list(1 / 2 * (vinf + cinf))

            Pbest = self.__agents[fitx.argmin()]
            if fitx.min() < self.Gbest_fit:
                Gbest = Pbest
                self.__agents = np.clip(self.__agents, lb, ub)
            flag = self.__set_flag(n, mr)
            self._points(self.__agents)

        self._set_Gbest(Gbest)

    def _set_Gbest(self, Gbest):
        self.__Gbest = Gbest

        
    def _points(self, agents):
        self.__Positions.append([list(i) for i in agents])

    def get_agents(self):
        """
        Returns a history of all agents of the algorithm (return type:
        list)
        """
        return self.__Positions


    def get_Gbest(self):
        """
        Return the best position of algorithm (return type: list)
        """
        return list(self.__Gbest)

    def __set_flag(self, n, mr):

        flag = [0 for i in range(n)]
        m = mr
        while m > 0:
            tmp = randint(0, n - 1)
            if flag[tmp] == 0:
                flag[tmp] = 1
                m -= 1

        return flag
    
    def __change_copy(self, copycat, cdc, crd):

        for i in range(len(copycat)):
            flag = [0 for k in range(len(copycat[i]))]
            c = cdc
            while c > 0:
                tmp = randint(0, len(copycat[i]) - 1)
                if flag[tmp] == 0:
                    c -= 1
                    copycat[i][tmp] = copycat[i][tmp] + choice([-1, 1]) * crd

        return copycat


    
    def __get_inf(self, i, velocity, cat, csi):

        if i == 0:

            vinf = np.array(velocity[i]) + (csi * np.array(velocity[1]) + (
                1 - csi) * np.array(velocity[2])) / 2 + \
                   (csi * np.array(velocity[-1]) + (1 - csi) * np.array(
                       velocity[-2])) / 2

            cinf = np.array(cat[i]) + (csi * np.array(cat[1]) + (1 - csi) *
                                       np.array(cat[2])) / 2 + \
                (csi * np.array(cat[-1]) + (1 - csi) * np.array(cat[-2])) / 2

        elif i == 1:

            vinf = np.array(velocity[i]) + (csi * np.array(velocity[2]) + (
                1 - csi) * np.array(velocity[3])) / 2 + \
                   (csi * np.array(velocity[0]) + (1 - csi) * np.array(
                       velocity[-1])) / 2

            cinf = np.array(cat[i]) + (csi * np.array(cat[2]) + (
                            1 - csi) * np.array(cat[3])) / 2 + \
                (csi * np.array(cat[0]) + (1 - csi) * np.array(cat[-1])) / 2

        elif i == len(velocity) - 1:

            vinf = np.array(velocity[i]) + (csi * np.array(velocity[0]) + (
                1 - csi) * np.array(velocity[1])) / 2 + \
                   (csi * np.array(velocity[i - 1]) + (1 - csi) * np.array(
                       velocity[i - 2])) / 2

            cinf = np.array(cat[i]) + (csi * np.array(cat[0]) + (1 - csi
                        ) * np.array(cat[1])) / 2 + \
                   (csi * np.array(cat[i - 1]) + (1 - csi
                                                  ) * np.array(cat[i - 2])) / 2

        elif i == len(velocity) - 2:

            vinf = np.array(velocity[i]) + (csi * np.array(velocity[i + 1]
                                ) + (1 - csi) * np.array(velocity[0])) / 2 + \
                   (csi * np.array(velocity[i - 1]) + (1 - csi
                                        ) * np.array(velocity[i - 2])) / 2

            cinf = np.array(cat[i]) + (csi * np.array(cat[i + 1]
                                ) + (1 - csi) * np.array(cat[0])) / 2 + \
                   (csi * np.array(cat[i - 1]) + (1 - csi
                                                  ) * np.array(cat[i - 2])) / 2

        else:

            vinf = np.array(velocity[i]) + (csi * np.array(velocity[i + 1]) + (
                1 - csi) * np.array(velocity[i + 2])) / 2 + \
                (csi * np.array(velocity[i - 1]) + (1 - csi
                                            ) * np.array(velocity[i - 2])) / 2

            cinf = np.array(cat[i]) + (csi * np.array(cat[i + 1]
                                ) + (1 - csi) * np.array(cat[i + 2])) / 2 + \
                   (csi * np.array(cat[i - 1]) + (1 - csi
                                                  ) * np.array(cat[i - 2])) / 2

        return vinf, cinf