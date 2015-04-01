import pygame
from pygame.locals import *
from random import randint

import GM
import pacmanobjectmanager as objects
import pacmanglobals as glob

class Controller(GM.GameObject):
    def __init__(self, screen):
        self.screen = screen
        self.normal_state = ControllerState(self)
        self.lose_state = ControllerLoseState(self)

        ### Gameplay variables
        self.score = 0
        self.lives = 3

        self.fontsize = 24
        self.fontcolor = (128,255,255)
        self.font = pygame.font.Font(None, self.fontsize)
        self.background = pygame.Surface((32*4, self.fontsize*2))
        self.backgroundcolor = (128, 32,32)
        self.background.fill(self.backgroundcolor)
        strip = GM.Strip([self.background], 1)
        pos = (32*2, self.fontsize)
        GM.GameObject.__init__(self, pos, strip, ControllerState(self))
        
        ### Game constants
        self.pointsperdot = 10
        self.pointsperstar = 50
        self.pointsperghost = (200,400,800,1600)

        objects.control.add(self)

    def score_dot(self):
        self.score += self.pointsperdot

    def score_star(self):
        self.score += self.pointsperstar

    def score_ghost(self):
        numeaten = 0
        for g in objects.ghosts:
            if g.state.name == 'eaten':
                numeaten += 1
        self.score += self.pointsperghost[numeaten]

class ControllerState(GM.State):

    def execute(self):
        self.show_life_and_score()
        
    def show_life_and_score(self):
        obj = self.obj
        score = obj.font.render("Score: %s" % obj.score, 1, obj.fontcolor)
        lives = obj.font.render("Lives: %s" % obj.lives, 1, obj.fontcolor)
        obj.image.fill(obj.backgroundcolor)
        obj.image.blit(score, (0, 0))
        obj.image.blit(lives, (0, obj.fontsize))

class ControllerLoseState(ControllerState):

    def execute(self):
        self.show_life_and_score()
        font = pygame.font.Font(None, 128)
        text = font.render("Game Over!", 1, (200,200,255))
        scrn = GM.vector(glob.screensize)
        loser = GM.GameObject(scrn/2, GM.Strip([text], 1))
        loser.depth = -100
        objects.all.add(loser)
        self.change_state(self.obj.normal_state)

    
