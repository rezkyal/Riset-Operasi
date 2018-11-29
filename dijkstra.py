import math
import argparse
import os
import sys
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

from nodeDijkstra import Node

parser=argparse.ArgumentParser()
parser.add_argument('-src', '--source', dest='source', type=str, default='input.txt', help='Name of file to be used as input')

args = parser.parse_args()

SET = []

if not os.path.isfile(os.path.join(os.getcwd(),args.source)):
    sys.exit("Source file not found")
else:
    PATHFILE=args.source

def printGraph(graph,JENIS):
    fromNode=[]
    toNode=[]
    for index,node in enumerate(graph):
        source=str(index)+" - "+str(node.weight)
        for connectedNode in node.connectTo:
            destination=str(connectedNode.index)+" - "+str(connectedNode.weight)
            fromNode.append(source)
            toNode.append(destination)

    df=pd.DataFrame()
    df['from']=fromNode
    df['to']=toNode
    print(df)
    if JENIS:
        G=nx.from_pandas_edgelist(df,'from','to',create_using=nx.DiGraph())
    else:
        G = nx.from_pandas_edgelist(df, 'from', 'to', create_using=nx.Graph())
    nx.draw(G,with_labels=True,node_size=1500, arrows=JENIS)
    plt.show()

def readData():
    data=[]
    with open(PATHFILE) as file:
        content=file.readlines()
    for index,lines in enumerate(content):
        content[index]=lines.split()
    JUMLAHNODE=int(content[0][0])
    JENIS=int(content[1][0])
    print(JENIS)
    for index in range(0,JUMLAHNODE):
        SET.append(None)
        data.append(Node(index,0))

    for index in range(2,(len(content))): #iterasi sisanya
        fromNode=int(content[index][0]) #from
        to=int(content[index][1]) #to
        weight=int(content[index][2]) #weight
        vector=(to,weight)
        data[fromNode].addVector(vector)

        if JENIS == 0: #undirected graph (bolak-balik)
            fromNode = int(content[index][1])  # from
            to = int(content[index][0])  # to
            weight = int(content[index][2])  # weight
            vector = (to, weight)
            data[fromNode].addVector(vector)

    for index in range(0,JUMLAHNODE):
        data[index].convertVectorToNumpy()
    return data,JENIS

graph,JENIS=readData()
SET[0]=0
graph[0].startNode()
while None in SET:
    minimumWeight = math.inf  # variable untuk menyimpan nilai terkecil (untuk dijadikan leaf selanjutnya)
    minimumNode=None #menyimpan objek node terkecil
    minimumIndex=None #menyimpan index nilai terkecil
    sourceNode=None #untuk menghilangkan parameter leaf nantinya
    for index,node in enumerate(graph):
        if node.leaf:
            vector=node.vector
            for connectedNode in vector: #cek setiap node terhubung
                leafNode = graph[connectedNode['nodeIndex']] 
                if SET[connectedNode['nodeIndex']] == None: #node belum mendapatkan shortest path
                    newWeight=node.weight+connectedNode['vectorWeight'] #menghitung nilai weight node
                    if newWeight < minimumWeight: #jika lebih kecil dari minimumWeight
                        leafNode.weight = newWeight #simpan weight di node leaf
                        minimumWeight=leafNode.weight #update minimumWeight
                        minimumIndex=connectedNode['nodeIndex']
                        minimumNode=leafNode
                        sourceNode=node #update source nde
    minimumNode.leaf=True #minimum node menjadi leaf
    sourceNode.addConnectedNode(minimumNode)
    removeLeaf=True
    for nodeIndex in sourceNode.vector['nodeIndex']: #cek apakah semua cabang source node sudah menjadi leaf
        if SET[nodeIndex] == None :
            removeLeaf=False
    if removeLeaf:
        sourceNode.leaf=False
    SET[minimumIndex]=minimumWeight
print(SET)
printGraph(graph,JENIS)