import sys
from MeshViewer import Point3D, Face, Triangle, Quad, Object

def goatLoad():
    meshname = "model/goat.obj"
    o = Object()
    o.name = "Model"
    o = loadObj(meshname,o)

    return o

def drawGoat(env3d, object):
    object.display(env3d)

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