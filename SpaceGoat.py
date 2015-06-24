from OpenGL.GLE.exceptional import _lengthOfArgname

__author__ = 'rvferreira e laispc'

import sys

from OpenGL.GLU import *
from pygame.locals import *

from space import setLights, meteorLoad, meteorDraw, meteorMove
from goat import goatLoad, goatDraw, goatMove
from starfield import *
from goat import goatLoad, goatDraw, goatMove, isGoatSafe
from utils import Z_FAR, Z_NEAR, WINDOW_HEIGHT, WINDOW_WIDTH, load_sound

DEATH_TIMER = 200

def main():

    pygame.mixer.init()
    pygame.mixer.music.load('focus.mp3')
    pygame.mixer.music.play(-1)
    effect = load_sound('goat_yell.wav')

    size = width, height = WINDOW_WIDTH, WINDOW_HEIGHT

    screen = pygame.display.set_mode(size, OPENGL|DOUBLEBUF)
    pygame.display.set_caption("SpaceGoat")
    setLights()

    pygame.init()

    font = pygame.font.Font(None, 20)
    textSurface = font.render("SpaceGoat", True, (255,255,255,255), (0,0,0,255))
    textData = pygame.image.tostring(textSurface, "RGBA", True)
    glRasterPos3d(0,0,5)
    glDrawPixels(textSurface.get_width(), textSurface.get_height(), GL_RGBA, GL_UNSIGNED_BYTE, textData)

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45.0, width/float(height), Z_NEAR, Z_FAR)
    glEnable(GL_DEPTH_TEST)
    glMatrixMode(GL_MODELVIEW)

    fps = 60
    dt = 1.0/fps
    clock = pygame.time.Clock()

    goat = goatLoad()
    meteor, stars = [], []
    meteorLoad(meteor)
    starInit(stars)

    move = False
    collision = False
    timer = 0.0
    score = 0
    increase_score = True
    play_effect = True

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
        starMove(stars)

        print "score", score

        if (meteor[0].t[2] > goat.t[2] + goat.safeZ + meteor[0].safeZ) and meteor[0].passed == False:
            score = score + 1
            pygame.display.set_caption("Score: " + str(score))
            meteor[0].passed = True

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()

        if (isGoatSafe(goat, meteor) == False):
            collision = True

        if (collision):
            score = 0
            if play_effect: 
                effect.play()
                play_effect = False
            pygame.display.set_caption("Score: " + str(score))
            timer += 1.0
            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

            red = 1.0 - timer/DEATH_TIMER
            glClearColor(red,0,0,1)
            if timer > DEATH_TIMER:
                for m in meteor:
                    del meteor[0]
                timer = 0
                collision = False
                play_effect = True
        else:
            goatDraw(goat)
            meteorDraw(meteor)
            starDraw(stars)

        pygame.display.flip()

if __name__ == '__main__': main()
