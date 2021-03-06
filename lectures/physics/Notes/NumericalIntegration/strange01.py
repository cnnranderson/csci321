# numeric integration illustration
# Runge Kutta integration lorenz attractor

import pygame, time
from pygame.locals import *
from pygame.color import *
from numpy import *

pygame.init()
screen = pygame.display.set_mode((1200,900))
background = pygame.Surface(screen.get_size())
background.fill((128,128,255))

"""
The Lorenz attractor has strange forces acting on it, giving
rise to chaotic behavior
The velocities, however, ONLY depend on position.
"""

state = array((10, 10, 10), dtype=float)
sigma, beta, rho = 10.0, 8/3.0, 28.0

def d(state):
    x,y,z = state
    dx = sigma * (y - x)
    dy = x * (rho - z) - y
    dz = x * y - beta * z
    return array((dx, dy, dz))

def rungekutta(state, dt):
    k1 = d(state)
    k2 = d(state + k1 * dt/2)
    k3 = d(state + k2 * dt/2)
    k4 = d(state + k3 * dt)
    newstate = state + (k1 + 2*k2 + 2*k3 + k4) * dt/6
    return newstate
  
t = 0
dt = 0.01

screen.blit(background, (0,0))

clock = pygame.time.Clock()

rotation = 0*pi/4.0
s = sin(rotation)
c = cos(rotation)

def getpt(state):
    x,y,z = state
    xy = c*x + s*y
    return array((xy*16+500,z*16+80),dtype=int)

running = 1
try:
    while running:
       # clock.tick(60)
        for event in pygame.event.get():
            if event.type == QUIT:
                running = 0
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                running = 0
        rotation += 0.01
        oldpt = getpt(state)
        t += dt
        state = rungekutta(state, dt)
        point = getpt(state)
        pygame.draw.circle(background, (255,0,0), point, 1)
        screen.blit(background, (0,0))
        pygame.display.flip()

finally:
    pygame.quit()

