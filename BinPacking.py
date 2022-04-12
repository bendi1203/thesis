import sys
import os
import numpy as np

#Harmonic fit szerűséget írni (3 - 4 osztályra)

# optimumhoz hasonlítani a kimenetet, átlag stb., m* értékvel osztani a megoldást -> külön külön algoritmusra: átlag, legnagyobb érték, legkisebb, összehasonlítások

# c értékeket grafikonon ábrázolni

#bináris kereséssel keresni -> eddig pakolt ládákat rendezni vmilyen sorrendbe -> felező keresés

#bemenetet ritkítani 10-10 darab (min 100db)

#optimal beolvasása, szótárba(?) rendezése

#elérési útvonalak beállítása, hogy máshol is működjön

path = r"D:\Thesis\thesis\input_bison"  # nem működik input_bison-nal
os.chdir(path)

# minden ágon végigmenni különböző c -vel
def overload(c):
    if (0 <= c) and (c <= 3 / 2):
        s = sys.maxsize - 2
        return s

    elif (3 / 2 <= c) and (c <= 9 / 5):
        s = 1 + (1 / c)

    elif (9 / 5 <= c) and (c <= 14 / 3):
        s = 1 + 2 / (3 * c)

    else:
        s = 1 + 1 / (3 * c)
    return s * 100

def firstFitForOneItem(bins, remainingSpace, item, maxHeight):
    j = 0
    while j < bins:
        if remainingSpace[j] >= item:
            remainingSpace[j] -= item
            break
        j += 1
    if j == bins:
        remainingSpace.append(maxHeight - item)
        bins += 1

    # print(bins)
    return bins

def firstFit(maxHeight, data):
    usedBins = 1
    remainingSpace = []
    remainingSpace.append(maxHeight)

    for i in range(len(data)):
        usedBins = firstFitForOneItem(usedBins, remainingSpace, data[i], maxHeight)

    return usedBins

def bestFitForOneItem(bins, remainingSpace, item, maxHeight):
    j = 0
    minIndex = -1
    min = sys.maxsize - 1
    while j < bins:
        if remainingSpace[j] >= item:
            if min > remainingSpace[j] - item:
                min = remainingSpace[j] - item
                minIndex = j
        j += 1

    if minIndex != -1:
        remainingSpace[minIndex] = min
    else:
        remainingSpace.append(maxHeight - item)
        bins += 1
    return bins

def bestFit(maxHeight, data):
    usedBins = 1
    remainingSpace = []
    remainingSpace.append(maxHeight)

    for i in range(len(data)):
        usedBins = bestFitForOneItem(usedBins, remainingSpace, data[i], maxHeight)

    return usedBins

def worstFitForOneItem(bins, remainingSpace, item, maxHeight):
    j = 0
    minIndex = 0
    min = sys.maxsize
    while j < bins:
        if maxHeight - remainingSpace[j] < min:
            min = maxHeight - remainingSpace[j]
            minIndex = j
        j += 1

    if remainingSpace[minIndex] >= item:
        remainingSpace[minIndex] -= item
    else:
        remainingSpace.append(maxHeight - item)
        bins += 1
    return bins

def worstFit(maxHeight, data):
    usedBins = 1
    remainingSpace = []
    remainingSpace.append(maxHeight)

    for i in range(len(data)):
        usedBins = worstFitForOneItem(usedBins, remainingSpace, data[i], maxHeight)

    return usedBins

def read_text(fpath, x):
    i = 0
    maxHeight = overload(x)
    with open(fpath, 'r') as f:
        numberOfItems = f.readline()
        binCapacity = f.readline()
        data = f.readlines()
        dataInt = []
        for i in range(len(data)):
            dataInt.append(int(data[i]))
        resultFirstFit = firstFit(maxHeight, dataInt)
        resultBestFit = bestFit(maxHeight, dataInt)
        resultWorstFit = worstFit(maxHeight, dataInt)
        print(resultFirstFit,' - ',resultBestFit, ' - ', resultWorstFit)

def readOptimal(fpath):
    with open(fpath, 'r') as f:
        optimals = []
        a = True
        while a:
            line = f.readline()
            if(not line):
                a = False
                break
            v = line.split(sep="\t")
            optimals.append(v[1])
            optimals.append(v[3])
            optimals.append(v[5])
        print(optimals)

def readDirectory(x):
    for file in os.listdir():
        if file.endswith('.BPP'):
            fpath = f"{path}\{file}"
            read_text(fpath, x)
        if file.endswith('.TXT'):
            fpath = f"{path}\{file}"
            readOptimal(fpath)

for x in np.linspace(1,3,3):
    readDirectory(x)