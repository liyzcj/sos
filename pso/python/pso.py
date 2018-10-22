# -*- coding: utf-8 -*-
"""
Created on Mon Oct 22 00:20:52 2018

@author: liyz
"""
import numpy as np
import matplotlib.pyplot as plt
from particle import Particle
from function import *


class Pso():
    
    def __init__(self,
                 dim = 2,
                 size = 25,
                 iters = 100,
                 x = 100,
                 func=sphere,
                 v = 1):
        self.dim = dim
        self.size = size    # number of particles
        self.iters = iters  # number of iterations
        self.func = func    # the fit function
        self.x =(-x,x)      # limitation of position
        self.v = (-v,v)     # limitaion of velocity
        
    # Main interface
    def solution(self,c=(2, 2),top ='full',variant='main'):
        # Initial the particles
        particles = [Particle(i) for i in range(self.size)]
        for particle in particles:
            particle.position = np.random.rand(2) * (self.x[1]-self.x[0]) + self.x[0]
            particle.velocity = np.random.rand(2) * (self.v[1]-self.v[0]) + self.v[0]
            # Initial Pbest and Gbest
            particle.pbest = particle.position.copy()
        fbest = np.zeros(self.size)
        result = np.zeros(self.iters)
        # iterations
        for it in range(self.iters):
            
            for particle in particles:
                # update pbest for each particle
                fbest[particle.id] = particle.update_pbest(self.func)
        
            for particle in particles:
                # Update Gbest 
                if top == 'full':
                    pos = np.where(fbest == np.min(fbest))
                    particle.gbest = particles[pos[0][0]].pbest
                elif top == 'ring':
                    ## get neighbours id
                    if particle.id == self.size -1:
                        nearid = [particle.id-1,particle.id,0]
                    else:
                        nearid = [particle.id-1, particle.id, particle.id+1]
                    fnear = fbest[nearid]
                    pos = np.where(fnear == np.min(fnear))[0][0]
                    particle.gbest = particles[nearid[pos]].pbest
                elif top == '4-neighbours':
                    nearid = self.get_four_neighbers(particle.id)
                    fnear = fbest[nearid]
                    pos = np.where(fnear == np.min(fnear))[0][0]
                    particle.gbest = particles[nearid[pos]].pbest
                # Update velocity
                if variant == 'main':
                    particle.update_velocity(c, self.v)
                elif variant == 'weight':
                    ## weight is linear decreasing from 0.9 to 0.4
                    weight = 0.4 + 0.5 * (1 - it / self.iters)
                    particle.update_velocity(c, self.v, weight=weight)
                elif variant == 'constriction':
                    phi = 4.1
                    chi = 2 / np.abs(2 - phi - np.sqrt(phi ** 2 - 4 * phi))
                    particle.update_velocity(c, self.v,constrictor=chi)
                # update position
                particle.update_position(self.x);
            
            # save the best result in this iteration
            result[it] = np.min(fbest)
            
        return result
                
    def get_four_neighbers(self, index):
        # compute length of square
        r = int(np.sqrt(self.size))
        # generate a rxr square contains particle's id
        grid = np.arange(self.size).reshape(r,r)
        # compute row and column
        row = int(np.floor(index / r))
        column = int(index % r)
        
        # get the neighbers index
        ## up
        up = grid[row-1][column]
        ## down
        if row == r-1:
            down = grid[0][column]
        else:
            down = grid[row+1][column]
        ## left
        left = grid[row][column-1]
        ## right
        if column == r-1:
            right = grid[row][0]
        else:
            right = grid[row][column+1]
            
        return [up,down,left,right,index]
        
if __name__ == '__main__':
    
    pso = Pso(func=rosenbrock, x=2.048)
    result = pso.solution(top ='4-neighbours',variant='constriction')
    plt.plot(result)
    
                