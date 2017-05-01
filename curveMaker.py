import maya.cmds as mc
import math
from maya.OpenMaya import MVector, MFloatMatrix, MMatrix, MScriptUtil
import pymel.core as pm
import os
import sys


"""
NAME: 
    curveMaker.
AUTHOR:
    Bella Luk
    March 2017
USAGE: 
    Given a curve and a selection of faces, will duplicate the curves out of the vertices from the selection
"""


"""
    getPolyInfo:
        from current selection, gets the normals of the ith vertex of the selection list.
    parameters:
        an index of wanted vertex
    returns:
        a rather convoluted list of normals.  must be parsed through with getNorm()

"""
def getPolyInfo(inVertList, i):
    exp = mc.ls(inVertList, flatten = True)
    mc.select(clear = True)
    mc.select(exp[i])
    return mc.polyNormalPerVertex(query = True, xyz=True, rel = True)

#flattens a list of vertices into one long list
def flattenList(inVertList):
    exp = mc.ls(inVertList, flatten = True)
    mc.select(clear = True)
    return exp
    
    
"""
    getNorm(inList) gets the average normal of the vertex.  
    PARAMETERS: list of vertex normals from mc.polyNormalperVertex(), which gives ALL normals of verticies.
    RETURNS: an MVector of the average normal.

"""
def getNorm(inList): #assumes there is at least 1 vert in the list. 
    x, y, z = 0, 0, 0
    print x, y, z
    s = 0 #to count # of vects
    while (len(inList) > 0):
        x += inList[0]
        y += inList[1]
        z += inList[2]
        del inList[:3] #check here if you broke it
        s += 1
    return MVector(x/s, y/s, z/s)

#prints vector for debugging
def printVect(inVect):
    print '(', inVect.x, inVect.y, inVect.z, ')'    

"""
    getTangent(bCurve): finds the tangent vector of the first point of the inputted curve
    PARAMETERS: a curve
    RETURNS: an MVector
"""
def getTangent(bCurve):
    p1 = MVector(*mc.getAttr(bCurve + '.cv[0]')[0])
    p2 = MVector(*mc.getAttr(bCurve + '.cv[1]')[0])
    return p2 - p1

#to set Values of the matrix:
def setCell(inMat, inVal, inRow, inCol):
    MScriptUtil.setDoubleArray(inMat[inRow], inCol, inVal)

"""
    skewSymmCross(inVect): assumes input is a cross-product vector.  returns the skew-symmetric cross product matrix.
    PARAMETER: MVector
    RETURNS: MMatrix
"""
def skewSymmCross(inVect): 
    m = MMatrix() #CTOR: identity matrix
    setCell(m, inVect.z, 1, 0)
    setCell(m, -inVect.y, 2, 0)
    setCell(m, inVect.x, 2, 1)
    setCell(m, -inVect.z, 0, 1) 
    setCell(m, inVect.y, 0, 2)
    setCell(m, -inVect.x, 1, 2)
    for i in range(4):
        setCell(m, 0, i, i)
    return m

"""
    findRotation(inV1, inV2): finds the rotation matrix to rotate from inV1 to inV2
    PARAMETERS: inv1 & inV2 are MVectors
    RETURNS: MMatrix

"""

def findRotation(inV1, inV2): #from inV1 to inV2
    cross = inV1 ^ inV2
    theta = inV1.angle(inV2)
    s = cross.length() * math.sin(math.degrees(theta))
    c = (inV1 * inV2 )* math.sin(math.degrees(theta))
    skew = skewSymmCross(cross)
    skewSQ = skew * skew
    m = MMatrix() + skew +( skewSQ *((1 - c)/ (s * s)))

    return m

    """
    #trying a different rotation matrix, 
    #assumes T-> thing to rotate to; N -> vect of thing to rotate
def findRotation(T, N): 
    T.normalize();
    N.normalize();
    B = N ^ T #getting the binormal
    B.normalize()
    m = MMatrix() #makes an identity matrix
    setCell(m, T.x, 0, 0)
    setCell(m, T.y, 0, 1)
    setCell(m, T.z, 0, 2)
    setCell(m, B.x, 1, 0)
    setCell(m, B.y, 1, 1)
    setCell(m, B.z, 1, 2)
    setCell(m, N.x, 2, 0)
    setCell(m, N.y, 2, 1)
    setCell(m, N.z, 2, 2)
    for i in range(4):
        setCell(m, 0, i, 3)
        setCell(m, 0, 3, i)
    setCell(m, 1, 3, 3)
    return m"""
    

    
#helper function to print out matrices
def printMatrix(inM):
    for i in range(4):
        for j in range(4):
            
            print inM(i,j),
        print
        
        
"""
    flatMatrix(inM) takes in a MMatrix and flattens it to a list, to be read by xForm
    PARAMETERS: inM- MMAtrix
    RETURNS: a list of floats (?)
"""
def flatMatrix(inM):
    flatList = []
    for i in range(4):
        for j in range(4):
            flatList.append(inM(j, i))
    return flatList

#function to set the pivot of your curve to the first CV
def setPivotCurve():
    selList = pm.selected()
    for i in selList:
        pos = i.getShape().getCV(0)
        i.setPivots(pos)

def getPivCurve(inCurve):
    return MVector(*mc.getAttr(inCurve + '.cv[0]')[0])


"""
curveSelect()

from the current selection, pulls out the name of the curve. assumes that there's only one curve.

"""
def curveSelect():
    selList = mc.ls(sl = True, type = 'nurbsCurve', dag = True)
    return selList[0].split('|')[0]

#curveSelect()

"""
curveMaker()

>>where the magic happens.

meant to be used w/the GUI: so takes in user input and does the duplication of the curve, and the moving and...

eventually rotation
>>

"""

def curveMaker():
    inCurve = mc.textField("curveNameInput", query = True, text = True)
    #cTanVect = getTangent(inCurve)
    #cTanVect.normalize()    
    p1 = MVector(*mc.getAttr(inCurve+'.cv[0]')[0])
    vertList = mc.polyListComponentConversion(ff = True, tv = True) #gets verts from selected faces
    flatList = flattenList(vertList)
    mc.select(clear = True)
    for i in range(len(flatList)): 
        cName = 'dCurve' + str(i)
        v1 = MVector(*mc.pointPosition(flatList[i]))
        vNorm = getNorm(getPolyInfo(flatList, i))

        mc.select(clear = True)
        vNorm.normalize()
        mc.duplicate(inCurve, name = cName)
        mc.select(cName)
        setPivotCurve()
        mc.select(clear = True)
        #mc.move( v1.x, v1.y, v1.z, cName, rpr=1)
        #cTanVect = getTangent(cName)
        #cTanVect.normalize()
        cTan= mc.pointOnCurve(cName, nt = True )
        cTanVect = MVector(cTan[0], cTan[1], cTan[2])

        rotMat = findRotation(cTanVect, vNorm) #B

        #printMatrix(rotMat)
        pivot = getPivCurve(cName)
        #printVect(pivot)
        mc.xform(cName, matrix = flatMatrix(rotMat),  ws = True, piv = (pivot.x, pivot.y, pivot.z))
        mc.move( v1.x, v1.y, v1.z, cName, rpr=1)

        
        


#home = os.getenv("HOME")
#user = os.geteng("USER")
#sys.path.appent(os.path.join(home:home.find(user), user, "Desktop"))

###ui stuff?
mc.window(title = "curveMaker", width = 300, height = 200)
mc.columnLayout( "testColumn", adjustableColumn = True)
mc.text(label = "curveMaker: Select the faces to extrude from", width = 20, height = 20, backgroundColor = [0.2, 0.2, 0.2], parent = "testColumn")
mc.textField("curveNameInput", text = "Input name here")
cName = mc.textField("curveNameInput", query = True, text = True)
print cName
mc.button("curveButton", label = "OK", width = 50, height = 20, backgroundColor = [0.2, 0.2, 0.2], parent = "testColumn", command = 'curveMaker()')
mc.showWindow()

#curveMaker('myCurve')

"""
TO DO:
    Add in labels for text box
    Add sliders for x, y, z rotations
    Add in a label + text box for duplicated curve names
    



"""

