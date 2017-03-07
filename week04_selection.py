import os

print(mc.help("polySphere"))
mc.polyCube(name="bellaCube", axis = (1, 1, 1))
mc.polySphere(name = "bellaSphere")
mc.polyPlane(name = "bellaPlane")

#list selected nodes
selNodes = mc.ls(sl = True)
print selNodes

#select all objects by name using the * wildcard
mc.select("bella*")

