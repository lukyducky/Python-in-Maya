import maya.cmds as mc

def countFaces():    
    #selects all objects w/poly
    mc.select("p*")
    selNodes = mc.ls(sl = True, tr = True)
    print selNodes
    
#prints out # of faces of every polygon obj in the scene
    for i in range(len(selNodes)-1):
        faceCnt = mc.polyEvaluate(selNodes[i], face = True)
        print "object: %s, faces: %s"%(selNodes[i], faceCnt);

countFaces()