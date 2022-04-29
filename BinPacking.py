import sys
import os
import numpy as np
import math


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
    b = len(remainingSpace) - 1 #utolsó eleme a listának
    while a <= b: #elsőben a legkisebb maradék hely és a végén a legtöbb
        if remainingSpace[math.floor((a + b) / 2)] > toInsert: #első fele
            b = math.floor((a + b) / 2) - 1
        else: #második fele
            a = math.floor((a + b) / 2) + 1
    remainingSpace.insert(a, toInsert)

def firstFitForOneItem(bins, remainingSpace, item, maxHeight):
    a = 0
    b = len(remainingSpace) - 1  # utolsó eleme a listának
    while a <= b:  # elsőben a legkisebb maradék hely és a végén a legtöbb
        if remainingSpace[math.floor((a + b) / 2)] >= item:
            toInsert = remainingSpace[math.floor((a + b) / 2)] - item
            del remainingSpace[math.floor((a + b) / 2)]
            binary(remainingSpace, toInsert)
            return bins
        else:  # második fele
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
    for file in os.listdir():
        if file.endswith('.BPP'):
            fpath = f"{path}\{file}"
            read_text(fpath, x)

        elif file.endswith('.csv'):
            fpath = f"{path}\{file}"
            readOptimal(fpath)

for x in np.linspace(1,3,3):
    readDirectory(x)

