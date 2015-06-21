#!/usr/bin/env python

"""Draw a cube on the screen. every frame we orbit
the camera around by a small amount and it appears
the object is spinning. note i've setup some simple
data structures here to represent a multicolored cube,
we then go through a semi-unopimized loop to draw
the cube points onto the screen. opengl does all the
hard work for us. :]
"""

import pygame
from pygame.locals import *

try:
    from OpenGL.GL import *
    from OpenGL.GLU import *
except:
    print ('The GLCUBE example requires PyOpenGL')
    raise SystemExit

meteorID = None

#some simple data for a colored cube
#here we have the 3D point position and color
#for each corner. then we have a list of indices
#that describe each face, and a list of indieces
#that describes each edge

#coordinates of each vertex
CUBE_POINTS = (
    (0.5, -0.5, -0.5),  (0.5, 0.5, -0.5),
    (-0.5, 0.5, -0.5),  (-0.5, -0.5, -0.5),
    (0.5, -0.5, 0.5),   (0.5, 0.5, 0.5),
    (-0.5, -0.5, 0.5),  (-0.5, 0.5, 0.5)
)

#colors are 0-1 floating values
CUBE_COLORS = (
    (1, 0, 0), (1, 1, 0), (0, 1, 0), (0, 0, 0),
    (1, 0, 1), (1, 1, 1), (0, 0, 1), (0, 1, 1)
)

#faces
CUBE_QUAD_VERTS = (
    (0, 1, 2, 3), (3, 2, 7, 6), (6, 7, 5, 4),
    (4, 5, 1, 0), (1, 5, 7, 2), (4, 0, 3, 6)
)

CUBE_EDGES = (
    (0,1), (0,3), (0,4), (2,1), (2,3), (2,7),
    (6,3), (6,4), (6,7), (5,1), (5,4), (5,7),
)

TEXTURE = (
    (1,1), (1,0), (0,0), (0,1),
)


def drawcube():
    "draw the cube"
    allpoints = zip(CUBE_POINTS, CUBE_COLORS)
    tex_vextex = zip(TEXTURE)
    global meteorID
    print "Texture Id got here", meteorID
    #glColor3f( 1,1,1 )
    #glEnable( GL_TEXTURE_2D )
    #glBindTexture( GL_TEXTURE_2D, meteorID )

    #glBegin(GL_POLYGON)
    for face in CUBE_QUAD_VERTS:
        t = 0
        glColor3f( 1,1,1 )
        glEnable( GL_TEXTURE_2D )
        glBindTexture( GL_TEXTURE_2D, meteorID )
        glBegin(GL_POLYGON)
        t=0
        for vert in face:
            pos, color = allpoints[vert]
            #glColor3fv(color)
            glTexCoord2fv( tex_vextex[t] )
            glVertex3fv(pos)  
            t = t+1    
        glEnd()
        glDisable( GL_TEXTURE_2D )  
"""
    glColor3f(1.0, 1.0, 1.0)
    glBegin(GL_LINES)
    for line in CUBE_EDGES:
        for vert in line:
            pos, color = allpoints[vert]
            glVertex3fv(pos)

    glEnd()
"""

def loadTexture( imageName = None ):
    if imageName == None :
        sys.exit(1)
    ix = iy = 0
    image = ""
    print imageName, "is image Nmae."
    try:
        im = pygame.image.load( imageName )
    except:
        print "Could not open ", imageName
        
    try:
        # get image meta-data (dimensions) and data
        ix,iy, image = im.get_width(), im.get_height(), pygame.image.tostring(im,"RGBA",1); 
    except SystemError:
        # has no alpha channel, synthesize one, see the
        # texture module for more realistic handling
        ix,iy, image = im.get_width(), im.get_height(), pygame.image.tostring(im,"RGBX",1); 
    # generate a texture ID
    ID = glGenTextures(1)
    # make it current
    glBindTexture(GL_TEXTURE_2D, ID)
    glPixelStorei(GL_UNPACK_ALIGNMENT,1)
    # copy the texture into the current texture ID
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
    glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_MODULATE);

    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, ix, iy, 0, GL_RGBA, GL_UNSIGNED_BYTE, image)
    
    # return the ID for use
    print "Texture Id", ID
    return ID
    
def main():
    "run the demo"
    #initialize pygame and setup an opengl display
    pygame.init()
    pygame.display.set_mode((640,480), OPENGL|DOUBLEBUF) #display size, flags
    glEnable(GL_DEPTH_TEST)        #use our zbuffer

    global meteorID
    meteorID = loadTexture("img/meteor.jpg")
    print "Texture Id got", meteorID

    #setup the camera
    glMatrixMode(GL_PROJECTION)
    gluPerspective(45.0,640/480.0,0.1,100.0)    #setup lens; set up a perspective projection matrix
    glTranslatef(0.0, 0.0, -3.0)                #move back
    glRotatef(20, 0, 0, 1)                      #orbit higher
    glRotatef(20, 0, 1, 0)  


    while 1:
        #check for quit'n events
        event = pygame.event.poll()
        if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
            break

        #clear screen and move camera
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)

        #orbit camera around by 1 degree
        glRotatef(1, 1, 0, 0)                    

        drawcube()
        pygame.display.flip()
        pygame.time.wait(10)


if __name__ == '__main__': main()

