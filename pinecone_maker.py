import maya.cmds as mc

def createShape(s):
    obj = mc.polyCone(height = s, sy = 10)
    faceCnt = mc.polyEvaluate(obj[0], face = True)
    for i in range(0, faceCnt -2, 2):
        face = "%s.f[%s]"%(obj[0], i) #naming the new extruded faces
        mc.polyExtrudeFacet(face, ltz = 1, ls = [0.1, 0.1, 0.1]) #actually extruding
        
createShape(1)