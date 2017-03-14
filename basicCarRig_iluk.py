import maya.cmds as mc

mc.select("Cart")
car = mc.ls(sl = True, type = "transform")
mc.select(clear = True)
print car

wheels = []
mc.select("pCylinder*")
sel = mc.ls(sl = True, type = "transform")
for i in range(len(sel)):
    wheels.append(sel[i])
print wheels

const = -90.0

multNode = mc.createNode("multiplyDivide")
mc.setAttr(multNode+".input1X", const)

mc.connectAttr(car[0] + ".translateX", multNode + ".input2X")
for i in range(len(wheels)):
    mc.connectAttr(multNode + ".outputX", wheels[i] + ".rotateZ")