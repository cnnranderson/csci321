# numeric integration illustration
# Runge Kutta integration for a spring under Hook's law

import pygame, time
from pygame.locals import *
from pygame.color import *
from numpy import *

pygame.init()
screen = pygame.display.set_mode((640,480))
background = pygame.Surface(screen.get_size())
background.fill((128,128,255))
  
m = 10.0
k = 4.0
t = 0

state = array((20, 0, t), dtype=float)
rstate = state.copy()
mstate = state.copy()

def xt(state): return (int(state[2]*5), int(state[0]+480/2))

def d(state):
    x, v, t = state
    # force is proportional to displacement
    f = -k*x
    # f = ma
    a = f/m
    # deriv of position is velocity:
    dx = v
    # deriv of velocity is acceleration:
    dv = a
    # dt/dt:
    dt = 1
    return array((dx,dv,dt),dtype=float)
    
def midpoint(state, dt):
    k1 = d(state)
    k2 = d(state + k1 * dt/2)
    newstate = state + k2 * dt
    return newstate

def rungekutta(state, dt):
    k1 = d(state)
    k2 = d(state + k1 * dt/2)
    k3 = d(state + k2 * dt/2)
    k4 = d(state + k3 * dt)
    newstate = state + (k1 + 2*k2 + 2*k3 + k4) * dt/6.0
    return newstate
  
dt = 0.05

screen.blit(background, (0,0))

running = 1
while running:
    if t*5 < screen.get_width():
        pygame.draw.circle(background, (255,0,0), xt(state), 1)
        pygame.draw.circle(background, (0,255,0), xt(mstate), 1)
        #pygame.draw.circle(background, (0,0,255), xt(rstate), 1)
        screen.blit(background, (0,0))
        t += dt
        mstate = midpoint(mstate, dt)
        rstate = rungekutta(rstate, dt)
        state += d(state)*dt #/2.0
        #state += d(state)*dt/2.0
        pygame.display.flip()
    else:
        running = 0

clock = pygame.time.Clock()

waiting = 1
while waiting:
    clock.tick(30)
    for event in pygame.event.get():
        if event.type == QUIT:
            waiting = 0
        elif event.type == KEYDOWN and event.key == K_ESCAPE:
            waiting = 0
            
pygame.quit()

