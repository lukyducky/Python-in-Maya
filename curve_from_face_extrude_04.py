import maya.cmds as mc
import math
from maya.OpenMaya import MVector, MFloatMatrix

"""
NAME: 
    Curve-Selection tool.
AUTHOR:
    Bella Luk
    March 2017
USAGE: 
    Given a curve and a selection of faces, will duplicate the curves out of the vertices from the selection
    
    
TO DO: import getRotation or whatever it's called


"""
def printVect(inVect):
    print '(', inVect.x, inVect.y, inVect.z, ')' 

#put rest of functions here


mc.polySphere()


mc.curve(name ='myCurve', p = [(0, 1, 0), (0, 0, 0), (1, 1, 1), (1, 2, 3)])

#get selected faces
cSel = mc.ls(sl = True)
print "current selection" 
print cSel #gets current selection

#get verticies from those faces; save the first one as a vector
vertList = mc.polyListComponentConversion(ff = True, tv = True) #from current selection, gets the verticies of the faces
vert = mc.pointPosition(vertList[0])
v1 = MVector(*mc.pointPosition(vertList[0]))


#storing the 1st CV into Vectors for easy mathing
p1 = MVector(*mc.getAttr('myCurve.cv[0]')[0])<- first point of curve


#duplicates original curve, & translates it.  
mc.duplicate('myCurve', name = 'dCurve01')
mc.xform('dCurve01', translation = [v1.x, v1.y, v1.z]) 
mc.xform('dCurve01', matrix =
#JUST GET THE ROTATION TRANSFORMATION AND XFORM IT AGAIN.  OK.  cool.

