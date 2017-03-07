import maya.cmds as mc

#shape 1
donut = mc.polyTorus(name = "myDonut", radius = 5, sectionRadius = 4, subdivisionsX = 25)
print donut[1]
donutSubDiv = mc.polyTorus(donut[1], query = True, subdivisionsX = True)
mc.polyTorus(donut[1], edit = True, subdivisionsX = donutSubDiv + 5)

#shape 2
coneA = mc.polyCone(name = "myBall", height = 1.3, radius = 4)
print coneA[1]
coneH = mc.polyCone(coneA[1], query = True, height = True)
print coneH
mc.polyCone(coneA[1], edit = True, height = coneH * 3)

#shape 3
myCylin = mc.polyCylinder(name = "aTube", height = 10, radius = 0.75, subdivisionsY = 10)
print myCylin[1]
CylinRad = mc.polyCylinder(myCylin[1], query = True, radius = True)
mc.polyCylinder(myCylin[1],edit = True, radius = CylinRad * .96)