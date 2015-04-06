import numpy as N

import pygame, time
from pygame.locals import *
from pygame.color import *
import numpy as N
from particlesystem003 import *


#### Globals
pygame.init()
screen = pygame.display.set_mode((640,480))
backcolor = (128,128,255)
background = pygame.Surface(screen.get_size())
background.fill(backcolor)
myfont = pygame.font.Font(None, 24)


### Forces
def drag(k):
    def func(psystem):
        for i in range(psystem.n):
            psystem.incForce(i, -k*psystem.vel(i))
    return func
        
def spring(k, center = N.array((320.0, 240.0, 0.0))):
    def func(psystem):
        for i in range(psystem.n):
            psystem.incForce(i, -k*(psystem.pos(i) - center))
    return func

def springpairs(k):
    def func(psystem):
        for i in range(0, psystem.n, 2):
            f = -k*(psystem.pos(i) - psystem.pos(i+1))
            psystem.incForce(i, f)
            psystem.incForce(i+1, -f)
    return func

def gravity(k):
    def func(psystem):
        for i in range(psystem.n):
            for j in range(psystem.n):
                if i != j:
                    v = psystem.pos(i) - psystem.pos(j)
                    psystem.incForce(i, -k*v/N.sqrt(N.dot(v,v)))
    return func              

#### Utilities

def newSystem(n):
    w,h = screen.get_size()
    size = min(w,h)
    positions = N.random.random(3*n)*size/2.0 + size/3.0
    velocities = N.random.random(3*n)*2.0 - 1.0
    masses = N.random.random(n)*5.0
    return ParticleSystem(positions, velocities, masses)

def reset(n):
    screen.blit(background, (0,0))
    return newSystem(n)


def textout(ls, stepper, txtcolor = (0,0,0)):
    if stepper == EulerStep:
        rtext = myfont.render("Euler", 1, txtcolor)
    elif stepper == MidpointStep:
        rtext = myfont.render("Midpoint", 1, txtcolor)
    elif stepper == RungeKuttaStep:
        rtext = myfont.render("Runge Kutta", 1, txtcolor)
    textrec = rtext.get_rect()
    textrec.topleft = (0,0)
    backrec = textrec.copy()
    backrec.width = 200
    txtback = pygame.Surface(backrec.size)
    txtback.fill(backcolor)
    txtback.blit(rtext, textrec)
    screen.blit(txtback, backrec)
    for i,txt in enumerate(ls):
        rtext = myfont.render(txt, 1, txtcolor)
        textrec = rtext.get_rect()
        textrec.topleft = (0, (i+1)*22)
        screen.blit(rtext, textrec)
    
def main():
    nParticles = 20
    plotTime = False
    mytext = ['spring(0.05)']
    myforces = [eval(f) for f in mytext]
    mysystem = newSystem(20)
    mystepper = EulerStep
    stepperfactor = 4
    baseticks = 20

    clock = pygame.time.Clock()
    running = 1
    deltaT = 0.1
    stepsize = deltaT
    screen.blit(background, (0,0))

    while running:
        clock.tick(baseticks*stepperfactor)
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
                    mytext = ['spring(0.05)']
                elif event.key == K_F2:
                    mysystem = reset(nParticles)
                    mytext = ['spring(0.1)','drag(0.05)']
                elif event.key == K_F3:
                    mysystem = reset(nParticles)
                    mytext = ['gravity(5.0)']
                elif event.key == K_F4:
                    mysystem = reset(nParticles)
                    mytext = ['gravity(2)','drag(0.1)']
                elif event.key == K_F5:
                    mysystem = reset(nParticles)
                    mytext = ['gravity(2.0)', 'spring(0.2)']
                elif event.key == K_F6:
                    mysystem = reset(nParticles)
                    mytext = ['gravity(2.0)','spring(0.2)','drag(0.05)']
                elif event.key == K_F7:
                    mysystem = reset(nParticles)
                    mytext = ['spring(0.5)']
                elif event.key == K_F8:
                    mysystem = reset(nParticles)
                    mytext = ['springpairs(0.1)']
                elif event.key == K_1:
                    mystepper = EulerStep
                    stepperfactor = 4
                    stepsize = deltaT
                elif event.key == K_2:
                    mystepper = MidpointStep
                    stepperfactor = 2
                    stepsize = 2.0*deltaT
                elif event.key == K_3:
                    mystepper = RungeKuttaStep
                    stepperfactor = 1
                    stepsize = 4.0*deltaT

        myforces = [eval(f) for f in mytext]
        mystepper(mysystem, myforces, stepsize)
        
        if plotTime:
            mysystem.Draw(screen, time=True)
        else:
            screen.blit(background, (0,0))
            mysystem.Draw(screen)
        textout(mytext, mystepper)
        pygame.display.flip()

if __name__ == "__main__":
    try:
        main()
    finally:
        pygame.quit()

    
    
    
