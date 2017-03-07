import maya.cmds as mc

theSphere = mc.polySphere()[0]
theCube = mc.polyCube()[0]

const = 1.0/90.0

multNode = mc.createNode("multiplyDivide")
mc.setAttr(multNode+".input1X", const)


mc.connectAttr(theCube + ".rotateY", multNode + ".input2X")
mc.connectAttr(multNode + ".outputX", theSphere + ".translateY")