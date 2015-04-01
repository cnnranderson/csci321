import pygame
from pygame.locals import *
from random import randint

import GM
import pacmanglobals as glob
import pacmanobjectmanager as objects
import pacmanroommanager as rooms

def main():
    pygame.init()
    screen = pygame.display.set_mode(glob.screensize)
    rooms.nextroom(screen)
    clock = pygame.time.Clock()
    running = True;
    while running:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
                else:
                    for p in objects.pacman:
                        p.state.handlekey(event.key)
        objects.all.update()
        objects.all.clear(screen, rooms.background)
        pygame.display.update(objects.all.draw(screen))

        ### "Win"  (there is no winning in pacman...)
        if len(objects.dots) == 0:
            rooms.nextroom(screen)

    pygame.quit()

if __name__ == '__main__':
    try:
        main()
    finally:
        pygame.quit()
        
