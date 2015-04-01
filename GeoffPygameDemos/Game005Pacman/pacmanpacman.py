import pygame,time
from pygame.locals import *
from random import randint

import GM
import pacmanglobals as glob
import pacmanobjectmanager as objects
from pacmanpacmanstates import *

class Pacman(GM.GameObject):
    def __init__(self, pos):
        self.name = 'pacman'
        self.up_state = PacmanUpState(self)
        self.left_state = PacmanLeftState(self)
        self.down_state = PacmanDownState(self)
        self.right_state = PacmanRightState(self)
        self.state = self.right_state
        self.strip = GM.get_strip('pacright.bmp')
        GM.GameObject.__init__(self, pos, self.strip, self.state)
        self.depth = -10
        self.state.enter()
        self.state.targetvelocity = None
        objects.pacman.add(self)





        
