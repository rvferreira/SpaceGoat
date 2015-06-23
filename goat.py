# IMPORT OBJECT LOADER
from utils import *
import math

MAX_TRANS_X = 80
GOAT_X_ANGLE = -60
GOAT_Z_TRANS = -10
GOAT_SPEED = 3

def goatLoad():
    obj = OBJ("model/goat/goat.obj", swapyz=True)
    obj.r, obj.t = (GOAT_X_ANGLE,0), (0,Y_GAME_PLAN,GOAT_Z_TRANS)
    obj.safeX = 10
    obj.safeZ = 5
    return obj

def goatDraw(obj):
    if obj.t[0] < -MAX_TRANS_X:
        obj.t = (-MAX_TRANS_X, obj.t[1], obj.t[2])
    if obj.t[0] > MAX_TRANS_X:
        obj.t = (MAX_TRANS_X, obj.t[1], obj.t[2])
    objDraw(obj)

def goatMove(goat, dir):
    goat.t = (goat.t[0]+dir*GOAT_SPEED, goat.t[1], goat.t[2])

def isGoatSafe(goat, meteor):
	radius = goat.safeX + meteor[0].safeX
	posGoat = goat.t[0]
	posMeteor = meteor[0].t[0]
	distance = math.fabs(posGoat - posMeteor)
	if (distance > radius):
		return True

	radius = goat.safeZ + meteor[0].safeZ
	posGoat = goat.t[2]
	posMeteor = meteor[0].t[2]
	distance = math.fabs(posGoat - posMeteor)
	if (distance > radius):
		return True
	
	if posMeteor > 0:
		return True

	return False
