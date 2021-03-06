import maya.cmds as mc

#get selected faces
cSel = mc.ls(sl = True)
print cSel #gets current selection
    #check if they are faces
    
    #if yes... continue
#get the created curve

#get verticies from those faces.
vertList = mc.polyListComponentConversion(ff = True, tv = True) #from current selection, gets the verticies of the faces
print vertList

#extrude a copy of the selected curve from those verticies; first one is a vertex of the face.

myCurve = mc.curve(p = [(0, 1, 0), (0, 0, 0), (1, 1, 1), (1, 2, 3)])

# works up to here 3/8/17

def makeCurve(inVert, inCurve):
    vPoint = mc.pointPosition(inVert)
    points = [vPoint]
    for i in inCurve #use getAttr for Curves!!!  (look at curves online)
    
        inPoint = vPoint
        """
        for x in inCurve[i]
            inPoint[x] += inCurve[i][x]
        points.append(inPoint)
    print points"""
    
makeCurve(vertList[0], myCurve)  
    
    mc.curve(name = inName, p = [vPoint, vPoint + inCurve[1]])