import maya.cmds as mc
import math
from maya.OpenMaya import MVector, MMatrix, MScriptUtil

#mc.curve(name ='myCurve', p = [(0, 1, 0), (0, 0, 0), (1, 1, 1), (1, 2, 3)])

p1 = MVector(*mc.getAttr('myCurve.cv[0]')[0])
p2 = MVector(*mc.getAttr('myCurve.cv[3]')[0])


#to set Values of the matrix:

def setCell(inMat, inVal, inRow, inCol):
    MScriptUtil.setDoubleArray(inMat[inCol], inCol, inVal)


#assumes input is a vector. spits out the skew-symmetric cross product matrix
def skewSymmCross(inVect): 
    m = MMatrix() #CTOR: identity matrix
    m[1][0] = inVect.z #apparently you can't access like this why maya
    m[2][0] = -inVect.y
    m[2][1] = inVect.x
    m[0][1] = -inVect.z
    m[0][1] = inVect.y
    m[1][2] = -inVect.x
    for i in range(4):
        m[i][i] = 0
    return m

def findRotation(inV1, inV2):
    cross = inV1 ^ inV2
    theta = inV1.angle(inV2)
    s = cross.length() * math.degrees(math.sin(theta))
    c = inV1 * inV2 * math.degrees(math.cos(theta))
    #m = MMatrix() + 
    
    
def printMatrix(inM):
    for i in range(4):
        for j in range(4):
            print inM(i,j),
        print
mat = MMatrix()
printMatrix(mat)
setCell(mat, 15, 2, 2)
printMatrix(mat)
#skewSymmCross(p2)
findRotation(p1, p2)