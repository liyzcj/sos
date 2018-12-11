# -*- coding: utf-8 -*-
"""
Created on Mon Oct 22 00:20:52 2018

@author: liyz
"""
import numpy as np
import matplotlib.pyplot as plt
from particle import Particle

class Pso():
    
    def __init__(self,
                 func,
                 dim = 2,
                 size = 25,
                 iters = 100,):
        self.dim = dim
        self.size = size    # number of particles
        self.iters = iters  # number of iterations
        self.func = func    # the fit function
        # Function space
        self.x =(0, 1)      # limitation of position
        self.v = (-0.1, 0.1)     # limitaion of velocity
        
    # Main interface
    def solution(self,c=(2, 2),top ='full',variant='main'):
        # Initial the particles
        particles = [Particle(i) for i in range(self.size)]
        for particle in particles:
            particle.position = np.random.rand(2) * (self.x[1]-self.x[0]) + self.x[0]
            particle.velocity = np.random.rand(2) * (self.v[1]-self.v[0]) + self.v[0]
            # Initial Pbest and Gbest
            # particle.pbest = particle.position.copy()
        fbest = np.zeros(self.size)
        best_it = []
        positions = []
        # iterations
        for it in range(self.iters):
            poss = []
            for particle in particles:
                print("==========================ITER {}: Particle {}============================".format(it, particle.id))
                # update pbest for each particle
                particle.update_pbest(self.func)
                fbest[particle.id] = particle.fbest

                # save each particles position
                poss.append(particle.position.copy())
            positions.append(poss)
        
            for particle in particles:
                # Update Gbest 
                if top == 'full':
                    pos = np.argmin(fbest)
                    particle.gbest = particles[pos].pbest
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
                particle.update_position(self.x)
            
            # save the best result in this iteration
            best_value = np.min(fbest)
            particle_id = np.argmin(fbest)
            best_position = particles[particle_id].position.copy()
            best_it.append((best_position,best_value))
            # return the best particle of each iterators and every particles position
            result = {'values':best_it,'positions': positions}
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
    
    fipairs = [(1,3),(2,2),(3,1)]
    topologies = ['full', 'ring', '4-neighbours']
    variants = ['main', 'weight', 'constriction']
    
                