from random import randrange
from utils import *
 
MAX_STARS  = 250
STAR_SPEED = 2

def starsInit(stars):
  for i in range(MAX_STARS):
    star = (i-120, i-120, i-120)
    stars.append(star)
 
def starMoveAndDraw(screen, stars):

    for star in stars:
        # glColor3fv((150, 150, 150))
        glVertex3fv(star)

    glLoadIdentity()