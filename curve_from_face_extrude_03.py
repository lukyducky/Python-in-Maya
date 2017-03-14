import maya.cmds as mc

"""
>>>>

>CURVE EXTRUDER
"""

#get selected faces
cSel = mc.ls(sl = True)
print "current selection" 
print cSel #gets current selection
#get the created curve

#get verticies from those faces.
vertList = mc.polyListComponentConversion(ff = True, tv = True) #from current selection, gets the verticies of the faces
print "vert List: "
print vertList

vert = mc.pointPosition(vertList[0])
print vert

#extrude a copy of the selected curve from those verticies; first one is a vertex of the face.

#mc.curve(name ='myCurve', p = [(0, 1, 0), (0, 0, 0), (1, 1, 1), (1, 2, 3)])

# works up to here 3/8/17
#for i in range(len(myCurve))
point = mc.getAttr('myCurve.cv[0]')[0]
print point[0]
for i in range(len(vert))
    point[i] +=vert[i] #<= adding the vert value to the point value.
print point
#curve2 = mc.curve(point, point1, point2, point3)


"""
def makeCurve(inVert, inCurve):
    vPoint = mc.pointPosition(inVert) #get points of the thing.
    points = [vPoint]
    for i in inCurve #use getAttr for Curves!!!  (look at curves online)
    
        inPoint = vPoint
        #nX = 
        print vPoint
        
    
makeCurve(vertList[0], myCurve)  """


#for i in range(len(vert))

#mc.curve(name = "aCurve", p = [vertList[0]])