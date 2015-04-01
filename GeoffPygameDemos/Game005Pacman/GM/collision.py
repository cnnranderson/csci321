import pygame

"""
Don't want sprites to collide with themselves, so, made some simple
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
                