#!/usr/bin/env python

"""Draw a cube on the screen. every frame we orbit
the camera around by a small amount and it appears
the object is spinning. note i've setup some simple
data structures here to represent a multicolored cube,
we then go through a semi-unopimized loop to draw
the cube points onto the screen. opengl does all the
hard work for us. :]
"""
import random
import pygame
from pygame.locals import *

try:
    from OpenGL.GL import *
    from OpenGL.GLU import *
except:
    print ('The GLCUBE example requires PyOpenGL')
    raise SystemExit

meteorID = None
i = 0

#some simple data for a colored cube
#here we have the 3D point position and color
#for each corner. then we have a list of indices
#that describe each face, and a list of indieces
#that describes each edge

# size of cubes
L = 0.01

#coordinates of each vertex

CUBE_POINTS = (
    (L, -L, -L),  (L, L, -L),
    (-L, L, -L),  (-L, -L, -L),
    (L, -L, L),   (L, L, L),
    (-L, -L, L),  (-L, L, L)
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

def set_vertices(max_distance, min_distance):
    x_value_change = float(random.randrange(-100,100))/1000.0
    #y_value_change = float(random.randrange(-100,100))/1000.0
    y_value_change = 0

    z_value_change = random.randrange(-1*max_distance,-1*min_distance)
    #z_value_change = -1*max_distance

    #x_value_change = 0
    #y_value_change = 0
    #z_value_change = -1*max_distance

    new_vertices = []

    for vert in CUBE_POINTS:
        new_vert = []

        new_x = vert[0] + x_value_change
        new_y = vert[1] + y_value_change
        new_z = vert[2] + z_value_change

        new_vert.append(new_x)
        new_vert.append(new_y)
        new_vert.append(new_z)

        new_vertices.append(new_vert)

    return new_vertices

def drawcube(vertices):
    "draw the cube"
    allpoints = zip(vertices)
    tex_vextex = zip(TEXTURE)
    global meteorID
    #print "Texture Id got here", meteorID
    #glColor3f( 1,1,1 )
    #glEnable( GL_TEXTURE_2D )
    #glBindTexture( GL_TEXTURE_2D, meteorID )

    #glBegin(GL_POLYGON)
    for face in CUBE_QUAD_VERTS:
        t = 0
        #glColor3f( 1,1,1 )
        glEnable( GL_TEXTURE_2D )
        glBindTexture( GL_TEXTURE_2D, meteorID )
        glBegin(GL_POLYGON)
        t=0
        for vert in face:
            pos = allpoints[vert]
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
    #screen params
    WIDTH = 800
    HEIGHT = 600
    # distance between cubes
    min_distance = 1
    max_distance = 3
    #initialize pygame and setup an opengl display
    pygame.init()
    pygame.display.set_mode((WIDTH,HEIGHT), OPENGL|DOUBLEBUF) #display size, flags
    #glEnable(GL_DEPTH_TEST)        #use our zbuffer

    global meteorID
    meteorID = loadTexture("meteor.jpg")
    #print "Texture Id got", meteorID

    #setup the camera - look at point
    #glMatrixMode(GL_PROJECTION)
    gluPerspective(45.0,float(WIDTH/HEIGHT),0.1,max_distance)       #setup lens; set up a perspective projection matrix
    glTranslatef(random.randrange(-1,1),random.randrange(-1,1), -1)
    #glTranslatef(0.0, -0.3, -0.5)                                    #move up and forward
    #glRotatef(15, 1, 0, 0)                                          #orbit higher
    #glMatrixMode(GL_MODELVIEW)

    #x = glGetDoublev(GL_MODELVIEW_MATRIX)

    # cubes dictionary
    cube_dict = {}
    for x in range(15):
        cube_dict[x] =set_vertices(max_distance,min_distance)

    #look at point
    x_move = 0
    y_move = -0

    x_rot = 0
    y_rot = 0


    global i
    while 1:
        #check for quit'n events
        event = pygame.event.poll()
        if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
            break

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                x_move = 0.01
            if event.key == pygame.K_RIGHT:
                x_move = -0.01

            if event.key == pygame.K_UP:
                x_rot = 0.1
            if event.key == pygame.K_DOWN:
                x_rot = -0.1


        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                x_move = 0

            if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                x_rot = 0

        #camera values
        x = glGetDoublev(GL_MODELVIEW_MATRIX)
        camera_x = x[3][0]
        camera_y = x[3][1]
        camera_z = x[3][2]
        print "z camera", camera_z

        #clear screen and move camera
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)

        #translate
        y_move = 0
        x_move = 0
        x_rot = 0
        glTranslatef(x_move,y_move,0.01)
        #glRotate(x_rot, 0, 1, 0)
        


        #orbit camera around by 1 degree
        """
        glRotatef(1, 1, 0, 0) 
        glPushMatrix()
        drawcube()
        glPopMatrix()
        """

        # rotate rapha
        """
        glPushMatrix()
        #glRotatef(45, 0, 0, 1)
        glRotatef(i, 0, 0, 1)
        i=i-1                      
        drawcube()     
        glPopMatrix()

        drawcube()

        glRotatef(1, 0, 0, 1)
        """
        """
        # um cubo parado e outro vindo
        glPushMatrix()
        glTranslatef(i, 0, 0, 1)
        #glTranslatef(1, 0, 0, 1)
        i=i-1    
        #if i < -100:
        #    glTranslatef(-i, 0, 0, 1)
        #    i = 0
        # cubo parado                  
        drawcube(cube_dict[0])     
        glPopMatrix()

        # cubo mexendo
        drawcube(cube_dict[1])

        glTranslatef(1, 0, 0, 1)
        """

        for each_cube in cube_dict:
            drawcube(cube_dict[each_cube])

        # Who passed the screen?
        for each_cube in cube_dict:
            #print "x cube", cube_dict[each_cube][0][0]
            #print "y cube", cube_dict[each_cube][0][1] 
            print "z cube", cube_dict[each_cube][0][2] 
            if camera_z + L + 1 <= -1*cube_dict[each_cube][0][2]:
                print("passed a cube")
                # recycle cube
                new_max = int(-1*(camera_z-max_distance))
                new_min = int(-1*(camera_z-min_distance))
                cube_dict[each_cube] = set_vertices(new_max,new_min)
                #cube_dict[each_cube] = set_vertices(max_distance)

        pygame.display.flip()
        pygame.time.wait(10)


if __name__ == '__main__': main()
