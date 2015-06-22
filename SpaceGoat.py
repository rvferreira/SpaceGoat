__author__ = 'rvferreira e laispc'

import sys, random
import pygame
from space import Env3D
from pygame.locals import *

from goat import drawGoat, goatLoad

WINDOW_WIDTH = 640
WINDOW_HEIGHT = 480

def main():

    #initialise pygame
    size = width, height = WINDOW_WIDTH, WINDOW_HEIGHT
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("SpaceGoat")
    pygame.init()

    #Setup display text
    text = pygame.Surface((300, 200))
    font = pygame.font.Font(None, 20)
    white = (255,255,255)
    fontimg = font.render("SpaceGoat",1,white)
    text.blit(fontimg, (5,0))

    #Main loop
    fps = 60
    dt = 1.0/fps
    clock = pygame.time.Clock()

    random.seed()
    env3d = Env3D(screen,[WINDOW_WIDTH,WINDOW_HEIGHT])
    o = goatLoad()

    o.scale(100.0)
    o.rotateX(3.141592)
    o.rotateX(-0.3)

    while 1:
        a = 0
        screen.fill((0,0,0))
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.display.quit()
                sys.exit(0)

        #First draw text, so that object appears in front of it
        screen.blit(text,(0,0))

        drawGoat(env3d, o)

        pygame.display.update()
        clock.tick(fps)

if __name__ == '__main__': main()
