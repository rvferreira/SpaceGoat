__author__ = 'rvferreira e laispc'

import sys, random
import pygame

from OpenGL.GLU import *
from OpenGL.GL import *
from pygame.locals import *

from space import setLights, meteorLoad, meteorDraw, meteorMove
from goat import goatLoad, goatDraw, goatMove, isGoatSafe
from utils import Z_FAR, Z_NEAR

WINDOW_WIDTH = 640
WINDOW_HEIGHT = 480

def main():

    #initialise pygame
    size = width, height = WINDOW_WIDTH, WINDOW_HEIGHT

    screen = pygame.display.set_mode(size, OPENGL|DOUBLEBUF)
    pygame.display.set_caption("SpaceGoat")
    setLights()

    pygame.init()

    # #Setup display text
    # text = pygame.Surface((300, 200))
    # font = pygame.font.Font(None, 20)
    # white = (255,255,255)
    # fontimg = font.render("SpaceGoat",1,white)
    # text.blit(fontimg, (5,0))

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45.0, width/float(height), Z_NEAR, Z_FAR)
    glEnable(GL_DEPTH_TEST)
    glMatrixMode(GL_MODELVIEW)

    #Main loop
    fps = 60
    dt = 1.0/fps
    clock = pygame.time.Clock()

    goat = goatLoad()
    meteor = []
    meteorLoad(meteor)

    rotate = move = False

    collision_num = 0
    valid_collison = True

    while 1:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.display.quit()
                sys.exit(0)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    sys.exit()
                elif event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    if event.key == pygame.K_LEFT: dir = -1
                    else: dir = 1
                    move = True
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    dir = 0
                    move = False


        if move:
            goatMove(goat, dir)


        meteorMove(meteor)

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()

        goatDraw(goat)
        meteorDraw(meteor)

        if (isGoatSafe(goat, meteor) == False):
            if valid_collison:
                collision_num += 1
                valid_collison = False
                print "Collisions = ", collision_num
        else:
            valid_collison = True

        pygame.display.flip()

if __name__ == '__main__': main()
