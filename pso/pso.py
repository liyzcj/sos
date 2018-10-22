# -*- coding: utf-8 -*-
"""
Created on Mon Oct 22 00:20:52 2018

@author: liyz
"""
import numpy as np
import matplotlib.pyplot as plt
from particle import Particle
from function import sphere


class Pso():
    
    def __init__(self,
                 dim = 2,
                 w = 1,
                 size = 5,
                 iters = 100,
                 x = 5.12,
                 func=sphere,
                 v = 1):
        self.dim = dim
        self.w = w          # weight
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
                    pass
                elif top == '4-neighbours':
                    pass
            for particle in particles:
                # Update velocity
                if variant == 'main':
                    particle.update_velocity_main(c, self.v)
                elif variant == 'weight':
                    pass
                elif variant == 'constriction':
                    pass
                
                # update position
                particle.update_position(self.x);
            
            # save the best result in this iteration
            result[it] = np.min(fbest)
            
        print(result.shape)
        return result
                

if __name__ == '__main__':
    
    pso = Pso()
    result = pso.solution()
    plt.plot(result)
    
                