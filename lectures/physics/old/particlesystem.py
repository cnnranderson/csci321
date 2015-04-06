import numpy as N
import pygame

class Particle():
    def __init__(self, m, state):
        self.mass = float(m)
        self.state = N.array(state)
        self.force = N.zeros(3)

    def Draw(self, screen, color, a, b, time):
        if time:
            x = time
            y = self.state[b]
        else:
            x = self.state[a]
            y = self.state[b]
        s = 1 + int(self.mass)
        pygame.draw.circle(screen, color, (int(x),int(y)), s)

class ParticleSystem():
    def __init__(self, particles, time = 0.0):
        self.particles = particles
        self.n = len(particles)
        self.time = time

    def ClearForces(self):
        for p in self.particles:
            p.force = N.zeros(3)

    def Dims(self):
        return 6 * self.n

    def GetState(self):
        result = []
        for p in self.particles:
            result.extend(p.state)
        return N.array(result)

    def SetState(self, state):
        for i in range(self.n):
            self.particles[i].state = state[i*6:i*6+6]
        
    def Draw(self, screen, color=(255,0,0), a=0, b=1, time=False):
        if time:
            time = self.time*10.0
        for p in self.particles:
            p.Draw(screen, color, a, b, time)
        
def ParticleDeriv(psystem, computeForces):
    psystem.ClearForces()
    for force in computeForces:
        force(psystem)
    result = []
    for p in psystem.particles:
        result.extend(p.state[3:6])
        result.extend(p.force/p.mass)
    return N.array(result)
        
def EulerStep(psystem, computeForces, deltaT):
    state = psystem.GetState()
    derivs = ParticleDeriv(psystem, computeForces)
    psystem.SetState(state + derivs * deltaT)
    psystem.time += deltaT


    
