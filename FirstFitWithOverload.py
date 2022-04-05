import sys
import os

#Harmonic fit szerűséget írni (3 - 4 osztályra)

#új könyvtár kell, ha nem találok: akkor overload nélkülihez hasonlítani
path = r"D:\Thesis\thesis\input_bison"  # nem működik input_bison-nal
os.chdir(path)

cost = 2

# minden ágon végigmenni különböző c -vel
def overload(c):
    if (0 <= c) and (c <= 3 / 2):
        s = 1 + sys.maxsize

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

def firstFit(overloadCost, data):
    usedBins = 1
    maxHeight = overload(overloadCost)
    remainingSpace = []
    remainingSpace.append(maxHeight)

    for i in range(len(data)):
        usedBins = firstFitForOneItem(usedBins, remainingSpace, data[i], maxHeight)

    return usedBins

def bestFitForOneItem(bins, remainingSpace, item, maxHeight):
    j = 0
    minIndex = -1
    min = sys.maxsize
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

def bestFit(overloadCost, data):
    usedBins = 1
    maxHeight = overload(overloadCost)
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

def worstFit(overloadCost, data):
    usedBins = 1
    maxHeight = overload(overloadCost)
    remainingSpace = []
    remainingSpace.append(maxHeight)

    for i in range(len(data)):
        usedBins = worstFitForOneItem(usedBins, remainingSpace, data[i], maxHeight)

    return usedBins

def read_text(fpath):
    i = 0
    with open(fpath, 'r') as f:
        numberOfItems = f.readline()
        binCapacity = f.readline()
        data = f.readlines()
        dataInt = []
        for i in range(len(data)):
            dataInt.append(int(data[i]))
        resultFirstFit = firstFit(cost, dataInt)
        resultBestFit = bestFit(cost, dataInt)
        resultWorstFit = worstFit(cost, dataInt)
        print(resultFirstFit,' - ',resultBestFit, ' - ', resultWorstFit)

for file in os.listdir():
    if file.endswith('.BPP'):
        fpath = f"{path}\{file}"
        read_text(fpath)

# print("Használt ládák száma: ", firstFit( 1.17,[1, 0.9, 0.8, 0.7, 0.6, 0.5, 0.4, 0.3, 0.2, 0.1]))

# h: rekeszek száma
# wi: i-edik rekesznek a magassága (a benne lévő dobozok összemagassága)
# si: i-edik rekesznek a max magassága (ameddig pakolhatjuk a ládákat)
# pi: i-edik doboznak a magassága
# dj: j-edik rekesznek a fennmaradó része (ha oda raknánk be az i-edik dobozt)
# k: eredmény (result)
