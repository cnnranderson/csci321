import pygame
from pygame.locals import *
from random import randint

import GM
import pacmanglobals as glob
import pacmanobjectmanager as objects

class GhostState(GM.GameState):

    def random_turn(self):
        obj = self.obj
        if obj.aligned(glob.spritesize):
            if obj.willcollide(objects.walls) or randint(0,9) < 2:
                obj.velocity = None
                while obj.velocity == None:
                    for vel in glob.velocities:
                        if randint(0,3) == 0 and not obj.willcollide(objects.walls, vel):
                            obj.velocity = vel
                            break

class GhostBeginState(GhostState):

    def try_to_go_up(self):
        obj = self.obj
        if not obj.willcollide(objects.walls, glob.upvelocity):
            obj.velocity = glob.upvelocity
            self.change_state(obj.normal_state)
        elif obj.aligned(glob.spritesize):
            for vel in glob.velocities:
                if not obj.willcollide(objects.walls, vel):
                    obj.velocity = vel
                    break

    def enter(self):
        self.name = 'begin'
        obj = self.obj
        obj.pos = obj.startpos * 1.0
        obj.velocity = glob.zerovelocity
        self.alarm = 5

    def update_begin(self):
        self.alarm -= 1
        if self.alarm < 0:
            self.try_to_go_up()

class GhostNormalState(GhostState):

    def enter(self):
        self.name = 'normal'
        obj = self.obj
        obj.set_strip(obj.strips[obj.name])

    def update_begin(self):
        self.random_turn()

class GhostScaredState(GhostState):

    def enter(self):
        obj = self.obj
        self.name = 'scared'
        self.alarm = obj.time_scared
        obj.set_strip(GM.get_strip('scared.gif'))

    def update_begin(self):
        obj = self.obj
        self.random_turn()
        self.alarm -= 1
        if self.alarm == 0:
            self.change_state(obj.normal_state)

class GhostEatenState(GhostState):

    def enter(self):
        obj = self.obj
        self.name = 'eaten'
        self.alarm = obj.time_eaten
        obj.set_strip(GM.get_strip('justeyes.gif'))

    def update_begin(self):
        obj = self.obj
        self.random_turn()
        self.alarm -= 1
        if self.alarm == 0:
            self.change_state(obj.normal_state)

