import maya.cmds as mc
import math
from maya.OpenMaya import MVector, MMatrix, MScriptUtil

#mc.curve(name ='myCurve', p = [(0, 1, 0), (0, 0, 0), (1, 1, 1), (1, 2, 3)])

p1 = MVector(*mc.getAttr('myCurve.cv[0]')[0])
p2 = MVector(*mc.getAttr('myCurve.cv[3]')[0])


def printVect(inVect):
    print '(', inVect.x, inVect.y, inVect.z, ')'    

#to set Values of the matrix:

def setCell(inMat, inVal, inRow, inCol):
    MScriptUtil.setDoubleArray(inMat[inRow], inCol, inVal)


#assumes input is a vector. spits out the skew-symmetric cross product matrix
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

def findRotation(inV1, inV2):
    cross = inV1 ^ inV2
    theta = inV1.angle(inV2)
    s = cross.length() * math.degrees(math.sin(theta))
    c = inV1 * inV2 * math.degrees(math.cos(theta))
    skew = skewSymmCross(cross)
    skewSQ = skew * skew
    m = MMatrix() + skew +( skewSQ *(1 / 1 + c))
    return m
    
    
def printMatrix(inM):
    for i in range(4):
        for j in range(4):
            print inM(i,j),
        print
                
                
print "p2:"
print printVect(p2)
                
mat = MMatrix()
printMatrix(mat)
matS = skewSymmCross(p2)


print "skew-symmetric cross product matrix:"
printMatrix(matS)

print "did we find the rotation yet"
printMatrix(findRotation(p1, p2))