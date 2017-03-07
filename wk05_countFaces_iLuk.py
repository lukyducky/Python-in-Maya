import maya.cmds as mc

def cubeMaker(n):
    for i in range(n):
        mc.polyCube(w = 1, h = i, d = 1)
        mc.polySphere()
        
    mc.select("p*") #selecting by name & wildcard *
    sel = mc.ls(sl = True, type = "shape") #getting the list of currently selected things
    print sel

    for i in range(len(sel)):
        rescale = i + 1
        mc.move(rescale, rescale, 0, sel[i], r = True)

def countFaces():    
    #selects all objects w/poly
    mc.select("p*")
    selNodes = mc.ls(sl = True, tr = True)
    print selNodes
    
#prints out # of faces of every polygon obj in the scene
    for i in range(len(selNodes)-1):
        faceCnt = mc.polyEvaluate(selNodes[i], face = True)
        print "object: %s, faces: %s"%(selNodes[i], faceCnt);
cubeMaker(5)
countFaces()