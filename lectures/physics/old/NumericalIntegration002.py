import numpy as N

import pygame, time
from pygame.locals import *
from pygame.color import *
import numpy as N
from particlesystem import Particle, ParticleSystem

pygame.init()
screen = pygame.display.set_mode((640,480))
background = pygame.Surface(screen.get_size())
background.fill((128,128,255))

def drag(k):
    def func(psystem):
        for p in psystem.p:
            p.f += -k*p.v 
    return func
        
def spring(k, center):
    def func(psystem):
        for p in psystem.p:
            p.f += -k*(p.x - center)
    return func

def gravity(k):
    def func(psystem):
        for p in psystem.p:
            for otherp in psystem.p:
                if p != otherp:
                    v = p.x - otherp.x
                    p.f += -k*v/N.sqrt(N.dot(v,v))
    return func

def main():
    plotTime = 0
    myforces = [gravity(5.0)]
    mypositions = [100.0+N.random.random(3)*200.0 for i in range(20)]
    myparticles = [Particle(N.random.random()*5, x, x-x) for x in mypositions]
    mysystem = ParticleSystem(myparticles)

    clock = pygame.time.Clock()
    running = 1
    deltaT = 0.1
    screen.blit(background, (0,0))

    while running:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == QUIT:
                running = 0
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                running = 0

        mysystem.EulerStep(myforces, deltaT)
        
        if plotTime:
            mysystem.Draw(screen, time=True)
        else:
            screen.blit(background, (0,0))
            mysystem.Draw(screen)
        pygame.display.flip()

if __name__ == "__main__":
    try:
        main()
    finally:
        pygame.quit()

    
    
    
