import numpy as N

import pygame, time
from pygame.locals import *
from pygame.color import *
import numpy as N
from particlesystem import *


#### Globals
pygame.init()
screen = pygame.display.set_mode((640,480))
background = pygame.Surface(screen.get_size())
background.fill((128,128,255))
myfont = pygame.font.Font(None, 24)


### Forces
def drag(k):
    def func(psystem):
        for p in psystem.particles:
            p.force += -k*p.state[3:6]
    return func
        
def spring(k, center = N.array((320.0, 240.0, 0.0))):
    def func(psystem):
        for p in psystem.particles:
            p.force += -k*(p.state[0:3] - center)
    return func

def gravity(k):
    def func(psystem):
        for p in psystem.particles:
            for otherp in psystem.particles:
                if p != otherp:
                    v = p.state[0:3] - otherp.state[0:3]
                    p.force += -k*v/N.sqrt(N.dot(v,v))
    return func

#### Utilities
def newParticle(size):
    m = N.random.random()*5.0
    state = N.zeros(6)
    for i in range(3):
        state[i] = N.random.random()*size/2.0 + size/4.0
    for i in range(3):
        state[i+3] = N.random.random()*2.0
    return Particle(m, N.array(state))

def newSystem(n):
    w,h = screen.get_size()
    size = min(w,h)
    particles = [newParticle(size) for i in range(n)]
    return ParticleSystem(particles)

def reset(n):
    screen.blit(background, (0,0))
    return newSystem(n)

def textout(ls):
    for i,txt in enumerate(ls):
        rtext = myfont.render(txt, 1, (0,0,0))
        textrec = rtext.get_rect()
        textrec.topleft = (0, i*22)
        screen.blit(rtext, textrec)
    
def main():
    nParticles = 20
    plotTime = False
    myforces = [spring(0.1)]
    mytext = ["spring(0.1)"]
    mysystem = newSystem(20)

    clock = pygame.time.Clock()
    running = 1
    deltaT = 0.1
    screen.blit(background, (0,0))

    while running:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == QUIT:
                running = 0
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = 0
                elif event.key == K_F12:
                    mysystem = reset(nParticles)
                    plotTime = not plotTime
                elif event.key == K_F1:
                    mysystem = reset(nParticles)
                    myforces = [spring(0.1)]
                    mytext = ['spring(0.1)']
                elif event.key == K_F2:
                    mysystem = reset(nParticles)
                    myforces = [spring(0.1), drag(0.05)]
                    mytext = ['spring(0.1)','drag(0.05)']
                elif event.key == K_F3:
                    mysystem = reset(nParticles)
                    myforces = [gravity(5.0)]
                    mytext = ['gravity(5.0)']
                elif event.key == K_F4:
                    mysystem = reset(nParticles)
                    myforces = [gravity(2.0),drag(0.1)]
                    mytext = ['gravity(2)','drag(0.1)']
                elif event.key == K_F5:
                    mysystem = reset(nParticles)
                    myforces = [gravity(2.0),spring(0.2),drag(0.05)]
                    mytext = ['gravity(2.0)','spring(0.2)','drag(0.05)']

        EulerStep(mysystem, myforces, deltaT)
        
        if plotTime:
            mysystem.Draw(screen, time=True)
        else:
            screen.blit(background, (0,0))
            mysystem.Draw(screen)
        textout(mytext)
        pygame.display.flip()

if __name__ == "__main__":
    try:
        main()
    finally:
        pygame.quit()

    
    
    
