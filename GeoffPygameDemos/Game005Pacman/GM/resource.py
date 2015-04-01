""" A singleton module loosely based on the Caching Resource Module
in the pygame code repository by David Clark """

import pygame, os
from pygame.locals import *

__strips = {}
__backgrounds = {}
__sounds = {}

__stripdir = 'Strips'
__backgrounddir = 'Backgrounds'
__sounddir = 'Sounds'

def set_folders(strdir, bgdir, snddir):
    stripdir, backgrounddir, sounddir = strdir, bgdir, snddir
    
def load_sound(file):
    class NoneSound:
        def play(self): pass
    if not pygame.mixer or not pygame.mixer.get_init():
        sound = NoneSound()
    else:
        fullname = os.path.join(__sounddir, file)
        try:
            sound = pygame.mixer.Sound(fullname)
        except pygame.error, message:
            sound = NoneSound()
    __sounds[file] = sound
    
def get_sound(file):
    if not __sounds.has_key(file):  load_sound(file)
    return __sounds[file]

def get_default_image():
    """A pulsing red disk"""
    defname = '__gm_default_image_name__'
    if not __strips.has_key(defname):
        background = (0,0,0)
        foreground = (255,0,0)
        frames = 30
        size = 32
        surf = pygame.Surface((frames*size, size))
        surf.fill(background)
        circle = pygame.draw.circle
        for i in range(0,frames/2):
            circle(surf, foreground, (size/2+size*i, size/2), i)
        for i in range(frames/2, frames):
            circle(surf, foreground, (size/2+size*i, size/2), frames-i)
        __strips[defname] = surf
    return __strips[defname]

class Strip():
    def __init__(self, images, nframes):
        self.images = images
        self.nframes = nframes

def load_strip(file, config=None):
    fullname = os.path.join(__stripdir, file)
    try:
        strip = pygame.image.load(fullname)
    except pygame.error, message:
        strip = get_default_image()
    strip = strip.convert()
    if config is not None:
        width,height,ncol,n,sep = config
        if n < 1:
           n = int(strip.get_width()/width)
           ncol = n
    else:
        height = strip.get_height()
        width = height
        n = int(strip.get_width()/width)
        ncol = n
        sep = 0
    images = []
    for i in range(n):
        newimage = pygame.Surface((width,height))
        x = (sep+width)*(i % ncol)
        y = (sep+height)*(i / ncol)
        newimage.blit(strip,(0,0),(x,y,width,height))
        newimage.convert()
        newimage.set_colorkey(newimage.get_at((0,0)), RLEACCEL)
        images.append(newimage)
    __strips[file] = Strip(images, n)

def get_strip(file, config=None):
    if not __strips.has_key(file): load_strip(file, config)
    return __strips[file]

def load_background(file):
    fullname = os.path.join(__backgrounddir, file)
    try:
        background = pygame.image.load(fullname)
    except pygame.error, message:
        background = pygame.Surface((64,64))
        background.fill((200,200,255))
    background.convert()
    __backgrounds[file] = background

def get_background(file):
    if not __backgrounds.has_key(file):  load_background(file)
    return __backgrounds[file]