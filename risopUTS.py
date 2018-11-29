import numpy as np
from beautifultable import BeautifulTable
import math
import argparse
import os
import sys

parser=argparse.ArgumentParser()
parser.add_argument('-mthd', '--method', dest='method', type=int, default=0, help='Method to be used, 0 for Northwest, 1 for Least Cost, 2 for Vogel ')
parser.add_argument('-src', '--source', dest='source', type=str, default='input.txt', help='Name of file to be used as input')

args = parser.parse_args()

if (args.method > 2) or (args.method < 0):
    METHOD=0
else:
    METHOD=args.method

if not os.path.isfile(os.path.join(os.getcwd(),args.source)):
    sys.exit("Source file not found")
else:
    PATHFILE=args.source

def drawTable(goods,city,x,cost,demand,supply):
    usedDemand=['Demand']
    for data in demand :
        usedDemand.append(str(data))
    usedDemand.append('')
    table=BeautifulTable()
    table.column_headers=city
    for i,used in enumerate(x):
        row=[]
        for j,cell in enumerate(used):
            strCell=str(cell)+'                        '+str(cost[i][j])
            row.append(strCell)
        table.append_row(row)
    table.insert_column(0,'',goods)
    table.append_column('Supply',supply)
    table.append_row(usedDemand)
    print(table)

def drawTableVogel(goods,city,x,cost,demand,supply,penaltyDemand,penaltySupply):
    usedDemand=['Demand']
    for data in demand :
        usedDemand.append(str(data))
    usedDemand.append(str(np.sum(demand)))
    usedDemand.append('')
    usedPenaltyDemand=['Penalty']
    for data in penaltyDemand:
        usedPenaltyDemand.append(str(data))
    usedPenaltyDemand.append('')
    usedPenaltyDemand.append('')
    table=BeautifulTable()
    table.column_headers=city
    for i,used in enumerate(x):
        row=[]
        for j,cell in enumerate(used):
            strCell=str(cell)+'                        '+str(cost[i][j])
            row.append(strCell)
        table.append_row(row)
    table.insert_column(0,'',goods)
    table.append_column('Supply',supply)
    table.append_column('Penalty',penaltySupply)
    table.append_row(usedDemand)
    table.append_row(usedPenaltyDemand)
    print(table)

def final(goodsName, cityName, x, cost, printDemand, printSupply):
    print('Final')
    drawTable(goodsName, cityName, x, cost, printDemand, printSupply)
    print('Total ongkos=')
    total = 0
    string = ''
    for i, row in enumerate(cost):
        for j, cell in enumerate(row):
            if not np.isnan(x[i][j]):
                total += x[i][j] * cost[i][j]
                string += str(x[i][j]) + '*' + str(cost[i][j]) + ' + '
    string = string[:-3]
    print(string)
    print('=', total)

def cekOverlap(supply,demand,cost,jumlahSupply,jumlahDemand,goodsName,cityName):
    sumSupply=np.sum(supply)
    sumDemand=np.sum(demand)
    if sumSupply>sumDemand :
        cityName.append('Dummy')
        delta=sumSupply-sumDemand
        demand=np.append(demand,delta)
        cost=np.column_stack((cost,np.zeros((jumlahSupply,1))))
        jumlahDemand+=1
    elif sumDemand>sumSupply:
        goodsName.append('Dummy')
        delta=sumDemand-sumSupply
        supply=np.append(supply,delta)
        cost=np.append(cost,np.zeros((1,jumlahDemand)),axis=0)
        jumlahSupply+=1
    return supply,demand,cost,jumlahSupply,jumlahDemand,goodsName,cityName

def readData():
    with open(PATHFILE) as file:
        content=file.readlines()
    for index,lines in enumerate(content):
        content[index]=lines.split()

    jumlahDemand=int(content[0][0])
    jumlahSupply=int(content[0][1])

    goodsName=[]
    cityName=[]
    supply=[]
    demand=[]
    cost=[]
    for i in range(0,jumlahSupply):
        supply.append(int(content[1][i]))
        goodsName.append(content[2][i])
    for i in range(0,jumlahDemand):
        demand.append(int(content[3][i]))
        cityName.append(content[4][i])
    for i in range(0,jumlahSupply):
        baris=[]
        for j in range(0,jumlahDemand):
            baris.append(int(content[5+i][j]))
        cost.append(baris)
    supply, demand, cost, jumlahSupply, jumlahDemand, goodsName, cityName = cekOverlap(np.array(supply),np.array(demand),np.array(cost).astype('float'),jumlahSupply,jumlahDemand,goodsName,cityName)
    return supply, demand, cost, jumlahSupply, jumlahDemand, goodsName, cityName

def pojokKiri(supply,demand,cost,jumlahSupply,jumlahDemand,goodsName,cityName):
    step=0
    for i in range(0, jumlahSupply):
        def works(step):
            for j in range(0, jumlahDemand):
                if demand[j] == 0:
                    continue
                if supply[i] >= demand[j]:
                    x[i][j] = demand[j]
                    supply[i] -= demand[j]
                    demand[j] = 0
                    step += 1
                    print('Iteration -', step)
                    drawTable(goodsName, cityName, x, cost, printDemand, printSupply)
                else:
                    x[i][j] = supply[i]
                    demand[j] -= supply[i]
                    supply[i] = 0
                    step += 1
                    print('Iteration -', step)
                    drawTable(goodsName, cityName, x, cost, printDemand, printSupply)
                    return step
            return step

        step=works(step)
    final(goodsName, cityName, x, cost, printDemand, printSupply)


def ongkosTerkecil(supply,demand,cost,jumlahSupply,jumlahDemand,goodsName,cityName):
    step=0
    dtype = [('x', int), ('y', int), ('cost', int)]
    costList = []
    for i in range(0, jumlahSupply):
        for j in range(0, jumlahDemand):
            values = (i, j, cost[i, j])
            costList.append(values)
    costList = np.array(costList, dtype=dtype)
    costList = np.sort(costList, order='cost')
    for data in costList:
        xAxis = data['x']
        yAxis = data['y']
        costValue = data['cost']

        if demand[yAxis] != 0 and supply[xAxis] != 0:
            if supply[xAxis] >= demand[yAxis]:
                x[xAxis][yAxis] = demand[yAxis]
                supply[xAxis] -= demand[yAxis]
                demand[yAxis] = 0
                step += 1
                print('Iteration -', step)
                drawTable(goodsName, cityName, x, cost, printDemand, printSupply)
            else:
                x[xAxis][yAxis] = supply[xAxis]
                demand[yAxis] -= supply[xAxis]
                supply[xAxis] = 0
                step += 1
                print('Iteration -', step)
                drawTable(goodsName, cityName, x, cost, printDemand, printSupply)
    final(goodsName, cityName, x, cost, printDemand, printSupply)

def vogel(supply,demand,cost,jumlahSupply,jumlahDemand,goodsName,cityName):
    step = 0
    costPrint = cost.copy()
    while (not np.isnan(cost).all()):
        penaltyDemand = []
        penaltySupply = []
        cloneCostBaris = cost.copy()
        cloneCostKolom = np.transpose(cost)
        for baris in cloneCostBaris:
            temp = np.sort(baris)
            delta = temp[1] - temp[0]
            if np.isnan(delta) and not np.isnan(temp[0]):
                delta = temp[0]
            penaltySupply.append(delta)

        for kolom in cloneCostKolom:
            temp = np.sort(kolom)
            delta = temp[1] - temp[0]
            if np.isnan(delta) and not np.isnan(temp[0]):
                delta = temp[0]
            penaltyDemand.append(delta)

        penaltyDemand = np.array(penaltyDemand)
        penaltySupply = np.array(penaltySupply)
        if step == 0:
            print('Initial')
            drawTableVogel(goodsName, cityName, x, cost, printDemand, printSupply, penaltyDemand, penaltySupply)
        allPenalty = np.concatenate((penaltyDemand, penaltySupply))
        allPenaltyIndex = []
        for index, data in enumerate(allPenalty):
            penalty = (data, index)
            allPenaltyIndex.append(penalty)

        dtype = [('penalty', float), ('index', int)]
        allPenaltyIndex = np.array(allPenaltyIndex, dtype=dtype)
        allPenaltyIndex = np.sort(allPenaltyIndex, order='penalty')
        maximumPenalty = -1
        minimumPenaltyCost = math.inf
        for i in allPenaltyIndex:

            if i['penalty'] > maximumPenalty:
                if i['index'] >= (len(penaltyDemand) - 1):
                    index = i['index'] % len(penaltyDemand)
                    used = cost[:, index]
                else:
                    index = i['index']
                    used = cost[index, :]
                minimumPenaltyCost = math.inf
                maximumPenalty = i['penalty']
                targetIndex = i['index']
            elif i['penalty'] == maximumPenalty:
                if minimumPenaltyCost > np.min(used):
                    minimumPenaltyCost = np.min(used)
                    maximumPenalty = i['penalty']
                    targetIndex = i['index']

        if targetIndex > (len(penaltyDemand) - 1):
            xAxis = targetIndex % len(penaltyDemand)
            used = cost[xAxis, :]
            lowest = math.inf
            for index, data in enumerate(used):
                if (data != np.nan) and (data < lowest):
                    lowest = data
                    yAxis = index
                else:
                    continue
            axis = 1
        else:
            yAxis = targetIndex
            used = cost[:, yAxis]
            lowest = math.inf
            for index, data in enumerate(used):
                if (data != np.nan) and (data < lowest):
                    lowest = data
                    xAxis = index
                else:
                    continue
            axis = 0

        if supply[xAxis] >= demand[yAxis]:
            x[xAxis][yAxis] = demand[yAxis]
            supply[xAxis] -= demand[yAxis]
            demand[yAxis] = 0
            step += 1
            print('Iteration -', step)
        else:
            x[xAxis][yAxis] = supply[xAxis]
            demand[yAxis] -= supply[xAxis]
            supply[xAxis] = 0
            step += 1
            print('Iteration -', step)
        if axis:
            cost[xAxis, :] = np.nan
        else:
            cost[:, yAxis] = np.nan
        drawTableVogel(goodsName, cityName, x, cost, demand, supply, penaltyDemand, penaltySupply)
    cost = costPrint
    final(goodsName, cityName, x, cost, printDemand, printSupply)

supply,demand,cost,jumlahSupply,jumlahDemand,goodsName,cityName=readData()
x=np.full((jumlahSupply,jumlahDemand),np.nan)
printSupply=np.array(supply) # untuk ngeprint, gak diubah-ubah nilainya
printDemand=np.array(demand)

if METHOD == 0:
    print('Northwest Method')
    pojokKiri(supply,demand,cost,jumlahSupply,jumlahDemand,goodsName,cityName)
elif METHOD == 1:
    print('Least Cost Method')
    ongkosTerkecil(supply,demand,cost,jumlahSupply,jumlahDemand,goodsName,cityName)
else:
    print('Vogel Method')
    vogel(supply,demand,cost,jumlahSupply,jumlahDemand,goodsName,cityName)
