import maya.cmds as mc
import math
from maya.OpenMaya import MVector, MFloatMatrix
import pymel.core as pm
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
    return mc.polyNormalPerVertex(query = True, xyz=True)
    
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
    setCell(m, inVect.z, 1, 0) #3
    setCell(m, -inVect.y, 2, 0)
    setCell(m, inVect.x, 2, 1)
    setCell(m, -inVect.z, 0, 1) #3
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
def findRotation(inV1, inV2):
    cross = inV1 ^ inV2
    theta = inV1.angle(inV2)
    s = cross.length() * math.degrees(math.sin(theta))
    c = (inV1 * inV2 )* math.degrees(math.cos(theta))
    skew = skewSymmCross(cross)
    skewSQ = skew * skew
    m = MMatrix() + skew +( skewSQ *(1 / 1 + c))
    return m


    
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
            flatList.append(inM(i, j))
    return flatList

#function to set the pivot of your curve to the first CV
def setPivotCurve():
    selList = pm.selected()
    for i in selList:
        pos = i.getShape().getCV(0)
        i.setPivots(pos)

#mc.polySphere()
#mc.curve(name ='myCurve', p = [(4, 1, 2), (2, 2, 7), (0, 1, 4), (-1, 2, 3)])

def curveSelect():
    selList = mc.ls(sl = True, type = 'nurbsCurve', dag = True)
    return selList[0].split('|')[0]

curveSelect()


def curveMaker(inCurve):
    cTanVect = getTangent(inCurve)
    cTanVect.normalize()    
    p1 = MVector(*mc.getAttr(inCurve+'.cv[0]')[0])
    vertList = mc.polyListComponentConversion(ff = True, tv = True) #gets verts from selected faces
    #flatList = flattenList(vertList)
    mc.select(clear = True)
    for i in range(len(vertList)): #list is not flattened...
        
        v1 = MVector(*mc.pointPosition(vertList[i]))
        vNorm = getNorm(getPolyInfo(vertList, i))
        mc.select(clear = True)
        vNorm.normalize()
        mc.duplicate(inCurve, name = 'dCurve' + str(i))
        mc.select('dCurve' + str(i))
        setPivotCurve()
        mc.select(clear = True)
        mc.move( v1.x, v1.y, v1.z, 'dCurve' + str(i), rpr=1) 
         
        #rotMat = findRotation(cTanVect, vNorm)
        #printMatrix(rotMat)
        rotV = cTanVect.rotateBy(cTanVect.rotateTo(vNorm))
        rotV.normalize()
        mc.xform('dCurve' + str(i), rotation = [rotV.x, rotV.y, rotV.z]) 
        #mc.xform('dCurve01', matrix = flatMatrix(rotMat))

###ui stuff?
cmds.window(title = "curveMaker", width = 300, height = 200)
cmds.columnLayout( "testColumn", adjustableColumn = True)
cmds.text(label = "curveMaker: Select the curve & faces to extrude from", width = 20, height = 20, backgroundColor = [0.2, 0.2, 0.2], parent = "testColumn")
mc.textField("curveNameInput", text = "Input name here")
cName = 'mc.textField("curveNameInput", query = True, value = True)'
cmds.button("curveButton", label = "OK", width = 50, height = 20, backgroundColor = [0.2, 0.2, 0.2], parent = "testColumn", command = 'curveMaker(curveSelect())')


cmds.showWindow()



curveMaker('myCurve')

