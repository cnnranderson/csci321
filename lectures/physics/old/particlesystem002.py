import numpy as N
import pygame

class ParticleSystem():
    def __init__(self, state, masses, time = 0.0):
        self.state = state
        self.masses = masses
        self.n = len(masses)
        self.dims = len(state)
        assert(self.n*6 == self.dims)
        self.forces = N.zeros(self.n*3)
        self.derivs = N.zeros(self.dims)
        self.time = time

    def ClearForces(self):
        self.forces = N.zeros(self.dims)
        
    def Draw(self, screen, color=(255,0,0), a=0, b=1, time=False):
        if time:
            time = self.time*10.0
        for i in range(self.n):
            s = 1 + int(self.masses[i])
            if time:
                x = time
                y = self.state[i*6+a]
            else:
                x = self.state[i*6+a]
                y = self.state[i*6+b]
            pygame.draw.circle(screen, color, (int(x), int(y)), s)
        
def ParticleDeriv(psystem, computeForces):
    psystem.ClearForces()
    for force in computeForces:
        force(psystem)
    for i in range(psystem.n):
        low, med, hi = i*6, i*6+3, i*6+6
        psystem.derivs[low:med] = psystem.state[med:hi]
        psystem.derivs[med:hi] = psystem.forces[i*3:i*3+3]/psystem.masses[i]
        
def EulerStep(psystem, computeForces, deltaT):
    ParticleDeriv(psystem, computeForces)
    psystem.state = psystem.state + psystem.derivs*deltaT
    psystem.time += deltaT


    
