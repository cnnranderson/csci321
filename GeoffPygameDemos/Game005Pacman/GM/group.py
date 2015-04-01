
import pygame

class DepthGroup(pygame.sprite.RenderUpdates):
    """A renderupdates group that draws the sprites by depth,
       deeper ones first, that is, behind shallower ones.
       Modified from pygame source code, sorting the sprites
       before rendering."""

    def compare(self,a,b):
        if a.depth < b.depth: return 1
        elif a.depth > b.depth: return -1
        else: return 0
    
    def draw(self, surface, offsetx = 0, offsety = 0):
        sprites = self.sprites()
        sprites.sort(self.compare)
        spritedict = self.spritedict
        surface_blit = surface.blit
        dirty = self.lostsprites
        self.lostsprites = []
        dirty_append = dirty.append
        for s in sprites:
            r = spritedict[s]
            newrect = surface_blit(s.image, s.rect)
            if r is 0:
                dirty_append(newrect)
            else:
                if newrect.colliderect(r):
                    dirty_append(newrect.union(r))
                else:
                    dirty_append(newrect)
                    dirty_append(r)
            spritedict[s] = newrect
        return dirty

