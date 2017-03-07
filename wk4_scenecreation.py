import maya.cmds as mc
import os as os

mc.file(new = True, force = True)

for i in range(5): #procedurally making a bunch of polyCubes
    mc.polyCube(w = .2, h = .2, d = .2)


mc.select("pCube*") #selecting by name & wildcard *
sel = mc.ls(sl = True, type = "shape") #getting the list of currently selected things
print sel

for i in range(len(sel)):
    rescale = i + 1
    mc.move(rescale, rescale, 0, sel[i], r = True)
    mc.scale(rescale, rescale, rescale, sel[i], a = True)

mc.file(rename = os.path.join(os.getenv("HOME"),"wk04_iLuk.mb" ))
mc.file(save = True)