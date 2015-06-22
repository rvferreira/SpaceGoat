import random
from MeshViewer import Point3D

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