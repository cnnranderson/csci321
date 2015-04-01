import pygame
from utilities import *
from state import *

class SimpleObject(pygame.sprite.Sprite):
   """The simplest possible object,
   no data, just executes its state"""
   
   def __init__(self, state=None):
      if state: self.state = state
      else:  self.state = State()
      
   def update(self):
      self.state.execute()
         
class GameObject(SimpleObject):
   """An object for simple Game Maker type games,
   includes animated sprite strip,
   velocity, gravity, friction, etc.
   updating handled by corresponding GameState class"""
   
   def __init__(self, pos, strip, state=None):
      pygame.sprite.Sprite.__init__(self) 
      
      if state: self.state = state
      else: self.state = GameState(self)
      
      self.strip = strip
      self.image = self.strip.images[0]
      self.rect = self.strip.images[0].get_rect()
      self.pos = vector(pos)
      self.rect.center = self.pos
      
      self.depth = 0
      self.startpos = self.pos*1.0
      self.previouspos = self.pos*1.0
      
      self.velocity = vector((0.0, 0.0))
      self.gravity = vector((0.0, 0.0))
      self.friction = 0.0
      
      self.frame = 0
      self.image = self.strip.images[self.frame]
      self.aspeed = 1.0    ## animation speed

    #### Handle messages

   def willcollide(self, walls, vel=None):
      if vel == None: vel = self.velocity
      self.rect.move_ip(vel)
      result = spritecollideany(self, walls)
      self.rect.move_ip(-vel)
      return result

   def aligned(self, gridsize):
      """Return true if aligned with grid in x and y"""
      modpos = (self.pos % gridsize) + (gridsize/2)
      ## numpy:
      ## return (modpos.astype(int) == gridsize.astype(int)).all()
      ## Numeric:
      return N.alltrue(modpos.astype(int) == gridsize.astype(int))
   
   def int_pos(self):
      self.pos = self.pos.astype(int).astype(float)

   def set_strip(self, strip, sameframe=True):
      self.strip = strip
      if sameframe:
         self.frame %= self.strip.nframes
      else:
         self.frame = 0
      self.image = self.strip.images[int(self.frame)]
      self.rect = self.image.get_rect()
      self.rect.center = self.pos

   def nearer(self, a, b):
      p = self.pos
      ap = a.pos
      bp = b.pos
      return cmp(norm(ap - p), norm(bp - p))
   
   def nearest(self, walls):
      """Find nearest wall"""
      walls.sort(cmp=self.nearer)
      return walls[0]

   def bounce(self, walls, sound=None):
      """Bounce off nearest wall"""
      if not walls: return
      if sound: sound.play()
      
      ## Move back one time step
      self.pos -=  self.velocity
      
      wall = self.nearest(walls)
      
      ## Bounce either horizontally or vertically
      collisionvec = wall.pos - self.pos
      if abs(collisionvec[0]) > abs(collisionvec[1]):
         self.velocity[0] *= -1
      else:
         self.velocity[1] *= -1

   def stopat(self, walls, sound=None):
      """stop at nearest wall"""
      if not walls: return
      if sound: sound.play()
      
      wall = self.nearest(walls)
      sw,sh = self.rect.size
      ww,wh = wall.rect.size
      w = 0.5*(sw+ww)
      h = 0.5*(sh+wh)
      
      ## horizontally or vertically?
      collisionvec = wall.pos - self.pos
      ## move to adjacent
      if collisionvec[0] > 0:
         self.pos[0] = wall.pos[0] - w
      elif collisionvec[0] < 0:
         self.pos[0] = wall.pos[0] + w
      elif collisionvec[1] > 0:
         self.pos[1] = wall.pos[1] - h
      elif collisionvec[1] < 0:
         self.pos[1] = wall.pos[1] + h
      ## stop
      self.velocity = vector((0,0))

"""
Don't want sprites to 'collide' with themselves, so, made some simple
modifications to the pygame source code.
"""

def spritecollide(sprite, group, dokill=False):
    """pygame.sprite.spritecollide(sprite, group, dokill) -> list
       collision detection between sprite and group

       given a sprite and a group of sprites, this will
       return a list of all the sprites that intersect
       the given sprite, NOT INCLUDING THE ORIGINAL.
       all sprites must have a "rect" value, which is a
       rectangle of the sprite area. if the dokill argument
       is true, the sprites that do collide will be
       automatically removed from all groups."""
    crashed = []
    spritecollide = sprite.rect.colliderect
    if dokill:
        for s in group:
            if spritecollide(s.rect) and s != sprite:
                s.kill()
                crashed.append(s)
    else:
        for s in group:
            if spritecollide(s.rect) and s != sprite:
                crashed.append(s)
    return crashed

def groupcollide(groupa, groupb, dokilla=False, dokillb=False):
    """pygame.sprite.groupcollide(groupa, groupb, dokilla, dokillb) -> dict
       collision detection between group and group

       given two groups, this will find the intersections
       between all sprites in each group
       NOT INCLUDING THE ORIGINALS. it returns a
       dictionary of all sprites in the first group that
       collide. the value for each item in the dictionary
       is a list of the sprites in the second group it
       collides with. the two dokill arguments control if
       the sprites from either group will be automatically
       removed from all groups."""
    crashed = {}
    if dokilla:
        for s in groupa:
            c = spritecollide(s, groupb, dokillb)
            if c:
                crashed[s] = c
                s.kill()
    else:
        for s in groupa:
            c = spritecollide(s, groupb, dokillb)
            if c:
                crashed[s] = c
    return crashed

def spritecollideany(sprite, group):
    """pygame.sprite.spritecollideany(sprite, group) -> sprite
       finds any sprites that collide

       given a sprite and a group of sprites, this will
       return return any single sprite that collides with
       with the given sprite, NOT INCLUDING THE ORIGINAL.
       If there are no collisions
       this returns None.

       if you don't need all the features of the
       spritecollide function, this function will be a
       bit quicker.

       all sprites must have a "rect" value, which is a
       rectangle of the sprite area."""
    spritecollide = sprite.rect.colliderect
    for s in group:
        if spritecollide(s.rect) and s != sprite:
            return s
    return None
                
