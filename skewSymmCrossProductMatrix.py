import maya.cmds as mc
import math
from maya.OpenMaya import MVector, MMatrix, MScriptUtil

"""
MATH HELPER FUNCTIONS 
Bella Luk
March 2017

Helper functions for rotating points & vectors & such

TO DO: 
>>a checker if there is more than one normal from getPolyInfo output

"""


"""
    getPolyInfo:
        from current selection, gets the normals of the ith vertex of the selection list.
    parameters:
        an index of wanted vertex
    returns:
        a rather convoluted list of normals.  must be parsed through with getNorm()

"""
def getPolyInfo(i):
    cSel = mc.ls(sl = True)
    vertList = mc.polyListComponentConversion(ff = 1, tv = True) #from current selection, gets the verticies of the faces
    #mc.select(vertList)
    exp = mc.ls(vertList, flatten = True)
    mc.select(exp[i])
    return mc.polyNormalPerVertex(query = True, xyz=True)
    
    
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
        del inList[:3]
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
    c = inV1 * inV2 * math.degrees(math.cos(theta))
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