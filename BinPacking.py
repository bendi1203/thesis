import sys
import os
import numpy as np
import math

from matplotlib import pyplot as plt

path = r"D:\Thesis\thesis\input_bison"  # nem működik input_bison-nal
os.chdir(path)

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

def binary(remainingSpace, toInsert):
    a = 0
    b = len(remainingSpace) - 1
    while a <= b:
        if remainingSpace[math.floor((a + b) / 2)] > toInsert:
            b = math.floor((a + b) / 2) - 1
        else:
            a = math.floor((a + b) / 2) + 1
    remainingSpace.insert(a, toInsert)

def firstFitForOneItem(bins, remainingSpace, item, maxHeight):
    a = 0
    b = len(remainingSpace) - 1
    while a <= b:
        if remainingSpace[math.floor((a + b) / 2)] >= item:
            toInsert = remainingSpace[math.floor((a + b) / 2)] - item
            del remainingSpace[math.floor((a + b) / 2)]
            binary(remainingSpace, toInsert)
            return bins
        else:
            a = math.floor((a + b) / 2) + 1
    remainingSpace.append(maxHeight - item)
    bins += 1
    toInsert = remainingSpace[len(remainingSpace) - 1]
    del remainingSpace[len(remainingSpace) - 1]
    binary(remainingSpace, toInsert)
    return bins

def firstFit(maxHeight, data):
    usedBins = 1
    remainingSpace = []
    remainingSpace.append(maxHeight)
    remainingSpace.append(maxHeight)
    for i in range(len(data)):
        usedBins = firstFitForOneItem(usedBins, remainingSpace, data[i], maxHeight)

    return usedBins

def bestFitForOneItem(bins, remainingSpace, item, maxHeight):
    a = 0
    b = len(remainingSpace) - 1  # utolsó eleme a listának
    minIndex = -1
    min = sys.maxsize - 1
    while a <= b:  # elsőben a legkisebb maradék hely és a végén a legtöbb
        if remainingSpace[math.floor((a + b) / 2)] >= item:
            if min > remainingSpace[math.floor((a + b) / 2)] - item:
                min = remainingSpace[math.floor((a + b) / 2)] - item
                minIndex = math.floor((a + b) / 2)
            b = math.floor((a + b) / 2) - 1
        else:  # második fele
            a = math.floor((a + b) / 2) + 1
    if minIndex != -1:
        del remainingSpace[minIndex]
        binary(remainingSpace, min)
    else:
        remainingSpace.append(maxHeight - item)
        bins += 1
        toInsert = remainingSpace[len(remainingSpace) - 1]
        del remainingSpace[len(remainingSpace) - 1]
        binary(remainingSpace, toInsert)
    return bins

def bestFit(maxHeight, data):
    usedBins = 1
    remainingSpace = []
    remainingSpace.append(maxHeight)
    remainingSpace.append(maxHeight)
    for i in range(len(data)):
        usedBins = bestFitForOneItem(usedBins, remainingSpace, data[i], maxHeight)

    return usedBins

def worstFitForOneItem(bins, remainingSpace, item, maxHeight):
    if remainingSpace[len(remainingSpace) - 1] - item > 0:
        toInsert = remainingSpace[len(remainingSpace) - 1] - item
        del remainingSpace[len(remainingSpace) - 1]
        binary(remainingSpace, toInsert)
    else:
        remainingSpace.append(maxHeight - item)
        bins += 1
        toInsert = remainingSpace[len(remainingSpace) - 1]
        del remainingSpace[len(remainingSpace) - 1]
        binary(remainingSpace, toInsert)

    return bins

def worstFit(maxHeight, data):
    usedBins = 1
    remainingSpace = []
    remainingSpace.append(maxHeight)
    remainingSpace.append(maxHeight)
    for i in range(len(data)):
        usedBins = worstFitForOneItem(usedBins, remainingSpace, data[i], maxHeight)

    return usedBins

def read_text(fpath, x):
    i = 0
    maxHeight = overload(x)
    with open(fpath, 'r') as f:
        f.readline()
        f.readline()
        data = f.readlines()
        dataInt = []
        for i in range(len(data)):
            dataInt.append(int(data[i]))
        resultFirstFit = firstFit(maxHeight, dataInt)
        resultBestFit = bestFit(maxHeight, dataInt)
        resultWorstFit = worstFit(maxHeight, dataInt)
        print(resultFirstFit,' - ',resultBestFit, ' - ', resultWorstFit)
        return [resultFirstFit, resultBestFit, resultWorstFit]

def readOptimal(fpath):
    with open(fpath, 'r') as f:
        optimals = []
        optimalsInt = []
        a = True
        while a:
            line = f.readline()
            if(not line):
                a = False
                break
            v = line.split(sep=";") #\t
            optimals.append(v[1])
            optimals.append(v[3])
            optimals.append(v[5])
        for i in range(len(optimals)):
            optimalsInt.append(int(optimals[i]))
        return optimalsInt

def readDirectory(x):
    firstFitList = []
    bestFitList = []
    worstFitList = []
    for file in os.listdir():
        if file.endswith('.BPP'):
            fpath = f"{path}\{file}"
            data = read_text(fpath, x)
            firstFitList.append(data[0])
            bestFitList.append(data[1])
            worstFitList.append(data[2])

        elif file.endswith('.csv'):
            fpath = f"{path}\{file}"
            readOptimal(fpath)

    fig, ax = plt.subplots()

    ax.plot(firstFitList,  'g')
    ax.set_title('First-Fit algorithm')
    plt.show()

    fig, ax = plt.subplots()
    ax.plot(bestFitList,  'r--')
    ax.set_title('Best algorithm')
    plt.show()

    fig, ax = plt.subplots()
    ax.plot(worstFitList, 'b.')
    ax.set_title('Worst-Fit algorithm')
    plt.show()

    fig, ax = plt.subplots()
    ax.plot(firstFitList, 'g', bestFitList, 'r--', worstFitList, 'b.')
    ax.set_title('Summarized')
    plt.show()

for x in np.linspace(1,3,3):
    readDirectory(x)

