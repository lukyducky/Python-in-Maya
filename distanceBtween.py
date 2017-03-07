import maya.cmds as mc

my_shphere = mc.polySphere()[0] #grabs transform node already yay
my_plane = mc.polyPlane(w = 10, h = 10)[0]
my_cube = mc.polyCube()[0]

mc.move(0, 0, 10, my_cube)

distNode = mc.createNode("distanceBetween")

mc.connectATtr(my_sphere