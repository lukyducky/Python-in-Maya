import maya.cmds as mc


#example 4
loc = mc.spaceLocator()

newTx = 3
newSx = 2

mc.setAttr(loc[0]+"tx".newTx)
mc.setAttr(loc[0]+"scaleX".newSx)

#example 5

loc = mc.spaceLocator()
sx.mc.getAttr(loc[0]+"scale")
mc.settAttr(loc[0],".scaleX", 2*sx)
