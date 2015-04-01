import pygame
from pygame.locals import *
from random import randint

import GM
import pacmanobjectmanager as objects
from pacmanghosts import *
from pacmanpacman import *
from pacmancontroller import *

class Wall(GM.GameObject):
    def __init__(self, pos, strip):
        GM.GameObject.__init__(self, pos, strip)
        objects.walls.add(self)

class Dot(GM.GameObject):
    def __init__(self, pos):
        GM.GameObject.__init__(self, pos, GM.get_strip('dot.gif'))
        objects.dots.add(self)

class Star(GM.GameObject):
    def __init__(self, pos):
        GM.GameObject.__init__(self, pos, GM.get_strip('special.gif'))
        objects.stars.add(self)

        


        
