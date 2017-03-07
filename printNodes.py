'''
printNodes(): -> will print out all the nodes passed into it.

'''

import maya.cmds as mc

#getting all of our nodes

#nodes = mc.ls() #gets all nodes
nodes = mc.ls(type = "transform") #gets only transform nodes



def printNodes(*args):
        for i in args:
                print "node = %s; type = %s\n"%(i, mc.nodeType(i))

printNodes(*nodes) #printing from the list of nodes we got earlier


    
    
def printNodeType(inType)
    myNodes = mc.ls(type = str(inType))
    printNodes(*myNodes)
