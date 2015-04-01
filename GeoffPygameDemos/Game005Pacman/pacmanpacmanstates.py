import pygame,time
from pygame.locals import *
from random import randint

import GM
import pacmanglobals as glob
import pacmanobjectmanager as objects

class PacmanState(GM.GameState):

    def handlekey(self, key):
        obj = self.obj
        if key == K_UP or key == K_w:
            self.change_state(obj.up_state)
        elif key == K_LEFT or key == K_a:
            self.change_state(obj.left_state)
        elif key == K_DOWN or key == K_s:
            self.change_state(obj.down_state)
        elif key == K_RIGHT or key == K_d:
            self.change_state(obj.right_state)

    def update_begin(self):
        obj = self.obj
        if obj.willcollide(objects.walls):
            obj.velocity = glob.zerovelocity
        if (self.targetvelocity and
            obj.aligned(glob.spritesize) and
            not obj.willcollide(objects.walls, self.targetvelocity)):
            obj.velocity = self.targetvelocity
            obj.set_strip(self.targetstrip)
            self.targetvelocity = None

    def update_middle(self):
        obj = self.obj
        for dot in GM.spritecollide(obj, objects.dots):
            GM.get_sound('pacchomp.wav').play()
            dot.kill()
            for c in objects.control: c.score_dot()

        for star in GM.spritecollide(obj, objects.stars):
            star.kill()
            for c in objects.control: c.score_star()
            for ghost in objects.ghosts:
                if ghost.state.name != 'eaten':
                    ghost.state.change_state(ghost.scared_state)

        for ghost in GM.spritecollide(obj, objects.ghosts):
            if ghost.state.name == 'scared':
                GM.get_sound('ghosteaten.wav').play()
                for c in objects.control: c.score_ghost()
                ghost.state.change_state(ghost.eaten_state)
            elif ghost.state.name == 'normal':
                GM.get_sound('killed.wav').play()
                time.sleep(1)
                for c in objects.control:
                    c.lives -= 1
                    if c.lives > 0:
                        obj.pos = obj.startpos * 1.0
                        obj.state.change_state(obj.right_state)
                        for g in objects.ghosts:
                            g.state.change_state(g.begin_state)
                    else:
                        for p in objects.pacman: p.kill()
                        for c in objects.control: c.state.change_state(c.lose_state)

class PacmanUpState(PacmanState):
    def enter(self):
        self.targetvelocity = glob.upvelocity
        self.targetstrip = GM.get_strip('pacup.bmp')

class PacmanLeftState(PacmanState):
    def enter(self):
        self.targetvelocity = glob.leftvelocity
        self.targetstrip = GM.get_strip('pacleft.bmp')

class PacmanDownState(PacmanState):
    def enter(self):
        self.targetvelocity = glob.downvelocity
        self.targetstrip = GM.get_strip('pacdown.bmp')

class PacmanRightState(PacmanState):
    def enter(self):
        self.targetvelocity = glob.rightvelocity
        self.targetstrip = GM.get_strip('pacright.bmp')
        
