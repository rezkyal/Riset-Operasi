import numpy as np
import math

class Node:
    def __init__(self,index,weight): #inisiasi Node
        self.index=index
        self.weight=math.inf
        self.vector=[]
        self.leaf=False
        self.connectTo=[]

    def convertVectorToNumpy(self): #menconvert vector dari array menjadi numpy, serta mengurutkannya berdasarkan vectorweight
        dtype = [('nodeIndex', int), ('vectorWeight', int)]
        self.vector=np.array(self.vector,dtype=dtype)
        self.vector = np.sort(self.vector, order='vectorWeight')

    def startNode(self): #inisiasi node sebagai startNode
        self.leaf=True
        self.weight=0

    def addVector(self,vector): #addVector yang terhubung dengan node
        self.vector.append(vector)

    def addConnectedNode(self,Node): #menambah node yang memiliki shortest path
        self.connectTo.append(Node)
