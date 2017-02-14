'''
printNodes(): -> will print out all the nodes in the current scene

'''

import maya.cmds as mc


nodes = mc.ls()

def printNodes(*args):
        for i in args:
                print "node = %s; type = %s\n"%(i, mc.nodeType(i))

printNodes(*nodes)