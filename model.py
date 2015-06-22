import os, sys, pygame, random, math, string
from pygame.locals import *
from MeshViewer import Point3D, Face, Triangle, Quad, Object

ANGLE_STEP = 0.1

MAX_ANGLE_X = 0.2
MAX_ANGLE_Y = 0.3

INITIAL_ANGLE_X = 0
INITIAL_ANGLE_Y = 0

targetAngleX = 0.0
targetAngleY = 0.0

rotate_x = INITIAL_ANGLE_X
rotate_y = INITIAL_ANGLE_Y

keyfire = 1

#We use our own version of the env3d class
class Env3D:
    def __init__(self,screen,winsize):
    	self.winsize= winsize
    	self.zoom_factor = 1
    	self.light_vector_1 = Point3D (random.random(),random.random(),random.random())
    	self.light_vector_1.normalize()
    	self.light_vector_2 = Point3D (random.random(),random.random(),random.random())
    	self.light_vector_2.normalize()
    	self.screen = screen
    	self.wincenter = [winsize[0]/2, winsize[1]/2]
    	self.colorize = True

def loadObj(filename,o):
    try:
        fp = open(filename, "r")
    except:
        print "File: "+filename+" not found"
        sys.exit(1)
    for line in fp:
        if line.startswith('#'): continue
        values = line.split()
        if not values: continue
        if values[0] == 'v':
            v = map(float, values[1:4])
            o.points.append( Point3D(v[0],v[1],v[2]) )
        elif values[0] == 'f':
            p = []
            for v in values[1:]:
                w = v.split("/")
                p.append(w[0])
            #obj file uses 1 as base, adjust for indexing with -1
            o.faces.append( Triangle(int(p[0])-1,int(p[1])-1,int(p[2])-1))
    fp.close()
    return o

def animate(activekey,o):
    global rotate_y
    global rotate_x
    global targetAngleY
    global targetAngleX

    if activekey == "R":
        rotate_y += ANGLE_STEP
        angle = (rotate_y < targetAngleY) * ANGLE_STEP
        o.rotateY(angle)
        if rotate_y > targetAngleY:
            rotate_y = targetAngleY
    if activekey == "L":
        rotate_y -= ANGLE_STEP
        angle = (rotate_y >= -targetAngleY) * ANGLE_STEP
        o.rotateY(-angle)
        if rotate_y < -targetAngleY:
            rotate_y = -targetAngleY
    if activekey == "U":
        rotate_x += ANGLE_STEP
        angle = (rotate_x < targetAngleX) * ANGLE_STEP
        o.rotateX(angle)
        if rotate_x > targetAngleX:
            rotate_x = targetAngleX
    if activekey == "D":
        rotate_x -= ANGLE_STEP
        angle = (rotate_x > -targetAngleX) * ANGLE_STEP
        o.rotateX(-angle)
        if rotate_x < -targetAngleX:
            rotate_x = -targetAngleX


    return o

def main():

    meshname = "model/goat.obj"
    o = Object()
    o.name = "Model"
    o = loadObj(meshname,o)

    #initialise pygame
    size = width, height = 600, 400
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("PyObjViewer - A simple 3D viewer")
    pygame.init()

    #prepare 3d environment
    random.seed()
    env3d = Env3D(screen,[width,height])

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

    activekey = ""

    o.scale(100.0)
    o.rotateX(3.141592)
    o.rotateX(-0.3)

    global keyfire
    global rotate_y
    global rotate_x
    global targetAngleY
    global targetAngleX

    while 1:

        screen.fill((0,0,0))
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.display.quit()
                sys.exit(0)
            elif event.type == KEYDOWN and keyfire:
                if event.key == K_ESCAPE:
                    pygame.display.quit()
                    sys.exit(0)
            try:
                if keyfire:
                    if event.key == K_LEFT:
                        if targetAngleY == 0:
                            targetAngleY = -MAX_ANGLE_Y
                        else:
                            targetAngleY = 0
                        activekey = "L"
                    if event.key == K_RIGHT:
                        activekey = "R"
                    if event.key == K_UP:
                        activekey = "U"
                    if event.key == K_DOWN:
                        activekey = "D"
                    if event.key == K_SPACE:
                        activekey = "STOP"
                    keyfire = 0
                else:
                    keyfire += 1

            except:
                pass

        o = animate(activekey,o)

        #First draw text, so that object appears in front of it
        screen.blit(text,(0,0))

        #display the 3D object
        o.display(env3d)

        pygame.display.update()
        clock.tick(fps)

if __name__ == '__main__': main()
