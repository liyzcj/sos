# -*- coding: utf-8 -*-
"""
Created on Mon Oct 22 00:50:22 2018

@author: liyz
"""
import numpy as np

class Particle():
    
    def __init__(self, idn):
        self.id = idn
        self.position = np.zeros(2)
        self.velocity = np.zeros(2)
        self.pbest = np.zeros(2)
        self.gbest = np.zeros(2)
        
    def update_pbest(self, func):
        
        fitness = func(self.position)
        fbest = func(self.pbest)
        if fitness < fbest:
            self.pbest = self.position.copy()
            fbest = func(self.pbest)
        return fbest
        
    def update_velocity(self, c, v, **kw):
        
        if 'weight' in kw.keys():
            self.velocity = kw['weight'] * self.velocity + \
                c[0] * np.random.rand() * (self.pbest - self.position) + \
                c[1] * np.random.rand() * (self.gbest - self.position)
        elif 'constrictor' in kw.keys():
            self.velocity = kw['constrictor'] *(self.velocity + \
                c[0] * np.random.rand() * (self.pbest - self.position) + \
                c[1] * np.random.rand() * (self.gbest - self.position))
        else:
            self.velocity = self.velocity + \
                c[0] * np.random.rand() * (self.pbest - self.position) + \
                c[1] * np.random.rand() * (self.gbest - self.position)
        # limitition of velocity
        self.velocity[np.where(self.velocity > v[1])] = v[1]
        self.velocity[np.where(self.velocity < v[0])] = v[0]
    
        
    def update_position(self, x):
        self.position += self.velocity
        
        # limitation of position
        self.position[np.where(self.position > x[1])] = x[1]
        self.position[np.where(self.position < x[0])] = x[0]        