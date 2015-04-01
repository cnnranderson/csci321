import pygame
from pygame.locals import *
from random import randint

import GM
import pacmanglobals as glob
import pacmanobjectmanager as objects
from pacmanghoststates import *

class Ghost(GM.GameObject):
    def __init__(self, pos):
        self.begin_state = GhostBeginState(self)
        self.normal_state = GhostNormalState(self)
        self.scared_state = GhostScaredState(self)
        self.eaten_state =  GhostEatenState(self)
        self.strips = {'inky':GM.get_strip('monster1.gif'),
                       'pinky':GM.get_strip('monster3.gif'),
                       'blinky':GM.get_strip('monster4.gif'),
                       'clyde':GM.get_strip('monster5.gif')}
        GM.GameObject.__init__(self, pos, self.strips[self.name], self.begin_state)
        self.state.enter()
        self.depth = -10
        self.time_scared = 5*30
        self.time_eaten = 10*30
        objects.ghosts.add(self)

class Inky(Ghost):
    def __init__(self, pos):
        self.name = 'inky'
        Ghost.__init__(self, pos)

class Pinky(Ghost):
    def __init__(self, pos):
        self.name = 'pinky'
        Ghost.__init__(self, pos)

class Blinky(Ghost):
    def __init__(self, pos):
        self.name = 'blinky'
        Ghost.__init__(self, pos)

class Clyde(Ghost):
    def __init__(self, pos):
        self.name = 'clyde'
        Ghost.__init__(self, pos)


        
