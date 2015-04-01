""" singleton module to manage rooms for pacman demo """

import pygame,time

import GM
import pacmanglobals as glob
import pacmanobjectmanager as objects
from pacmanobjects import *

roomcolors = {'room1':  (32,32,64),
              'room2':  (64,32,32)}

wallstrip = 'walls.bmp'
walldict = {
  'F':0,
  'V':1,
  '<':2,
  'L':3,
  '^':4,
  'I':5,
  'o':6,
  '}':7,
  '>':8,
  'J':9,
  '-':10,
  'W':11,
  '7':12,
  '{':13,
  'M':14,
  '+':15
}
wallconfig = (32,32,8,16,1)
background = None

currentroom = -1
rooms = ('room1', 'room2')

def nextroom(screen):
    global currentroom, rooms
    currentroom += 1
    currentroom %= len(rooms)
    loadroom(rooms[currentroom], screen)

def loadroom(name, screen):
    global background
    if not background:
        background = pygame.Surface(glob.screensize)
        background = background.convert()
    background.fill(roomcolors[name])
    screen.blit(background, (0,0))
    pygame.display.flip()

    if len(objects.control) == 0:
        objects.control.add(Controller(screen))

    ## Remove everything but global objects:
    controller =  objects.control.sprites()[0]
    for obj in objects.all: obj.kill()
    objects.control.add(controller)

    ## Refill other objects:
    roomfile = 'Rooms/%s.txt' % name
    GM.loadroomtiles(roomfile,
                     walldict,
                     wallstrip,
                     wallconfig, 
                     Wall)
    GM.loadroomobjects(roomfile, '.', Dot, glob.spritesize)
    GM.loadroomobjects(roomfile, '*', Star, glob.spritesize)
    GM.loadroomobjects(roomfile, 'e', Pacman, glob.spritesize)
    GM.loadroomobjects(roomfile, 'i', Inky, glob.spritesize)
    GM.loadroomobjects(roomfile, 'b', Blinky, glob.spritesize)
    GM.loadroomobjects(roomfile, 'p', Pinky, glob.spritesize)
    GM.loadroomobjects(roomfile, 'c', Clyde, glob.spritesize)

    objects.all.add(objects.walls,
                    objects.dots,
                    objects.stars,
                    objects.pacman,
                    objects.ghosts,
                    objects.control)

    GM.get_sound('gamebeginning.wav').play()


