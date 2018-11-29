import numpy as np
import math
import collections
from copy import copy

def readData(): #berfungsi untuk membaca data, mencari ukuran tabel serta isinya
    data = []
    with open(input_path) as file:
        content = file.readlines()
    for index, lines in enumerate(content):
        content[index] = lines.split()
    square = int(content[0][0])
    content = content[1:]
    for x in range(0, square):
        row = []
        for y in range(0, square):
            row.append(int(content[x][y]))
        data.append(row)
    return data,square

def deleteRow(data): #berfungsi untuk menghapus angka pada baris, sesuai angka terkecil yang ada di baris itu
    for indexR, row in enumerate(data):
        indexDel=np.argmin(row)
        lowest=int(data[indexR][indexDel])
        for indexC, column in enumerate(row):
            data[indexR][indexC]-=lowest
    return data

def deleteColumn(data): #berfungsi untuk menghapus angka pada kolom, sesuai angka terkecil yang ada di kolom itu
    data=np.transpose(data)
    for indexR, row in enumerate(data):
        indexDel=np.argmin(row)
        lowest=int(data[indexR][indexDel])
        for indexC, column in enumerate(row):
            data[indexR][indexC]-=lowest
    data=np.transpose(data)
    return data

def satuGarisRow(data,garisRow,garisColumn,square,highest): #fungsi rekursi untuk mencari garis yang harus dihapus berdasarkan perspektif baris, dilengkapi dengan backtrack ketika ada garis yang tidak sesuai
    data_lama=copy(data)
    garisRow_lama=copy(garisRow)
    garisColumn_lama=copy(garisColumn)
    highest_lama=copy(highest)
    
    founded=False
    for index, row in enumerate(data):
        sumZero = collections.Counter(row)
        if sumZero[0] == highest:
            garisRow[index] = 1
            data[index] = np.full((square,), 1, dtype=int)
            founded=True
            break
     
    
    if 0 not in data:   
        if 1 not in garisColumn:
            return data,garisRow,garisColumn,False
        else:
            return data,garisRow,garisColumn,True
    
    if founded:
        data,garisRow,garisColumn,nilai=satuGarisRow(data,garisRow,garisColumn,square,highest)
        if not nilai:
            data,garisRow,garisColumn,nilai=satuGarisColumn(data_lama,garisRow_lama,garisColumn_lama,square,highest_lama)
    else:
        data,garisRow,garisColumn,nilai=satuGarisColumn(data,garisRow,garisColumn,square,highest)
        if not nilai:
            data,garisRow,garisColumn,nilai=satuGarisRow(data_lama,garisRow_lama,garisColumn_lama,square,highest_lama-1)

    
    return data,garisRow,garisColumn,True

def satuGarisColumn(data,garisRow,garisColumn,square,highest): #fungsi rekursi untuk mencari garis yang harus dihapus berdasarkan perspektif kolom dilengkapi dengan backtrack ketika ada garis yang tidak sesuai
    data_lama=copy(data)
    garisRow_lama=copy(garisRow)
    garisColumn_lama=copy(garisColumn)
    highest_lama=copy(highest)
    
    founded=False
    data = np.transpose(data)
    
    for index, row in enumerate(data):
        sumZero = collections.Counter(row)
        if sumZero[0] == highest:
            garisColumn[index] = 1
            data[index] = np.full((square,), 1, dtype=int)
            founded=True
            break

            
    data = np.transpose(data)
 
    if 0 not in data:
        if 1 not in garisRow:
            return data,garisRow,garisColumn,False
        else:
            return data,garisRow,garisColumn,True
    
    if founded:
        data,garisRow,garisColumn,nilai=satuGarisColumn(data,garisRow,garisColumn,square,highest)
        if not nilai:
            data,garisRow,garisColumn,nilai=satuGarisRow(data_lama,garisRow_lama,garisColumn_lama,square,highest_lama-1)
    else:
        data,garisRow,garisColumn,nilai=satuGarisRow(data,garisRow,garisColumn,square,highest-1)
        if not nilai:
            data,garisRow,garisColumn,nilai=satuGarisColumn(data_lama,garisRow_lama,garisColumn_lama,square,highest_lama-1)

        
    return data,garisRow,garisColumn,True
    
def garisin(data, garisRow, garisColumn,square): #fungsi utama untuk menggaris, mencari nilai 0 terbesar dari tabel, lalu masuk kedalam fungsi rekursi
    highest = 0
    for index, row in enumerate(data):
        sumZero = collections.Counter(row)
        if sumZero[0] > highest:
            highest = sumZero[0]
    for index, row in enumerate(np.transpose(data)):
        sumZero = collections.Counter(row)
        if sumZero[0] > highest:
            highest = sumZero[0]
    
    data,garisRow,garisColumn,nilai = satuGarisRow(data,garisRow,garisColumn,square,highest)
    return data,garisRow,garisColumn

def deleteAfter(data, garisColumn,garisRow): #fungsi untuk mengurangi isi tabel ketika jumlah garis tidak sama dengan ukuran tabel
    lowest=math.inf
    for row,dataRow in enumerate(data):
        for column,dataColumn in enumerate(dataRow):
            if (garisColumn[column] == 0) and (garisRow[row] == 0):
                if data[row][column] < lowest:
                    lowest=data[row][column]
    
    for row,dataRow in enumerate(data):
        for column,dataColumn in enumerate(dataRow):
            if (garisColumn[column] == 0) and (garisRow[row] == 0):
                data[row][column] -= lowest
            elif (garisColumn[column] == 1) and (garisRow[row] == 1):
                data[row][column] += lowest
    
    return data

def cellZero(data, row, column, nolRow, nolColumn, selectedCell, square): #fungsi rekursi untuk mencari (x,y) angka 0 yang akan digunakan pada perhitungan akhir, dilengkapi dengan backtrack untuk melihat jika angka 0 yang dipilih ternyata salah
    nolRow_lama = copy(nolRow)
    nolColumn_lama = copy(nolColumn)
    selectedCell_lama = copy(selectedCell)
    row_lama = copy(row)
    column_lama = copy(column)
    if row == square:
        return nolRow, nolColumn, selectedCell, True
    if data[row][column] == 0:
        if nolRow[row] == 0 and nolColumn[column] == 0:
            selectedCell.append((row, column))
            nolRow[row] = 1
            nolColumn[column] = 1
            nolRow, nolColumn, selectedCell, nilai = cellZero(
                data, row + 1, 0, nolRow, nolColumn, selectedCell, square)
            if nilai:
                return nolRow, nolColumn, selectedCell, True
            else:
                return cellZero(data, row_lama, column_lama + 1, nolRow_lama,
                                nolColumn_lama, selectedCell_lama, square)
        else:
            if column == (square - 1) and row == (square - 1):
                return nolRow, nolColumn, selectedCell, True
            elif column == (square - 1):
                return nolRow, nolColumn, selectedCell, False
            else:
                return cellZero(data, row, column + 1, nolRow, nolColumn,
                                selectedCell, square)
    else:
        if column == (square - 1) and row == (square - 1):
            return nolRow, nolColumn, selectedCell, True
        elif column == (square - 1):
            return nolRow, nolColumn, selectedCell, False
        else:
            return cellZero(data, row, column + 1, nolRow, nolColumn,
                            selectedCell, square)


def selectZero(data, square): #fungsi utama untuk mencari posisi angka 0 untuk perhitungan di akhir
    selectedCell = []
    nolRow = np.zeros((square, ), dtype=int)
    nolColumn = np.zeros((square, ), dtype=int)
    nolRow, nolColumn, selectedCell, nilai = cellZero(
        data, 0, 0, nolRow, nolColumn, selectedCell, square)
    return nolRow, nolColumn, selectedCell, nilai


input_path='input_am.txt'

#read data dari file
data,square = readData()
data = np.array(data)
data_ori=copy(data) #data asli disimpan untuk perhitungan di akhir

print("Data awal")
print(data)

#mengurangi angka dengan angka paling kecil di baris/kolomnya
data=deleteRow(data)
data=deleteColumn(data)

print("Setelah mengurangi dengan angka paling kecil di baris/kolomnya")
print(data)

#menggarisi tabel
garisRow=np.zeros((square,), dtype=int)
garisColumn=np.zeros((square,), dtype=int)
data_lama=copy(data)
data_baru,garisRow,garisColumn=garisin(data,garisRow,garisColumn,square)
data=data_lama


jumlahGaris=0
jumlahGaris+=np.count_nonzero(garisRow)
jumlahGaris+=np.count_nonzero(garisColumn)
while jumlahGaris != square: #jika jumlah garis yang tergambar tidak sama dengan ukuran tabel
    data=deleteAfter(data,garisColumn,garisRow) #fungsi untuk mengurangi isi tabel ketika jumlah garis tidak sama dengan ukuran tabel

    #menggarisi tabel
    garisRow=np.zeros((square,), dtype=int)
    garisColumn=np.zeros((square,), dtype=int)
    data_lama=copy(data)
    data_baru,garisRow,garisColumn=garisin(data,garisRow,garisColumn,square)
    data=data_lama

    jumlahGaris=0
    jumlahGaris+=np.count_nonzero(garisRow)
    jumlahGaris+=np.count_nonzero(garisColumn)

#memilih lokasi angka 0 yang akan dipakai pada perhitungan akhir
nolRow,nolColumn,selectedCell,nilai=selectZero(data,square)

print("Setelah jumlah garis=ukuran tabel")
print(data)

print("Cell yang terpilih")
print(selectedCell)

#print akhir
hasil=0
output=""
for cell in selectedCell:
    angka=data_ori[cell[0]][cell[1]]
    output+=str(data_ori[cell[0]][cell[1]])+" + "
    hasil+=angka
output=output[:-3]
print("Hasil akhir adalah:")
print(output)
print(hasil)