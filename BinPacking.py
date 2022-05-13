import sys
import os
import math

from matplotlib import pyplot as plt

path = r"D:\Thesis\thesis\input_bison"
os.chdir(path)

def overload(c):
    if (0 <= c) and (c < 3 / 2):
        s = sys.maxsize - 2
        return s

    elif (3 / 2 <= c) and (c < 9 / 5):
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
    j = 0
    while j < bins:
        if remainingSpace[j] >= item:
            remainingSpace[j] -= item
            break
        j += 1
    if j == bins:
        remainingSpace.append(maxHeight - item)
        bins += 1
    return bins


def firstFit(maxHeight, data):
    usedBins = 1
    remainingSpace = []
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
        if remainingSpace[math.floor((a + b) / 2)] >= item: # bin.beszúrással megkeressük, hogy mibe fogjuk belerakni az elemet
            if min > remainingSpace[math.floor((a + b) / 2)] - item:
                min = remainingSpace[math.floor((a + b) / 2)] - item
                minIndex = math.floor((a + b) / 2)
            b = math.floor((a + b) / 2) - 1
        else:
            a = math.floor((a + b) / 2) + 1
    if minIndex != -1: # kivesszük az elemet és binary() megkeresi az új helyet
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
    if remainingSpace[-1] == maxHeight:
        return usedBins
    else:
        return usedBins + 1


def worstFitForOneItem(bins, remainingSpace, item, maxHeight):
    if remainingSpace[len(remainingSpace) - 1] != maxHeight:
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
    else:
        if remainingSpace[len(remainingSpace) - 2] - item > 0:
            toInsert = remainingSpace[len(remainingSpace) - 2] - item
            del remainingSpace[len(remainingSpace) - 2]
            binary(remainingSpace, toInsert)
        else:
            remainingSpace[len(remainingSpace) - 1] -= item
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
    if remainingSpace[-1] == maxHeight:
        return usedBins
    else:
        return usedBins + 1

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
        # print(resultFirstFit,' - ',resultBestFit, ' - ', resultWorstFit)
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
            v = line.split(sep=";")
            optimals.append(v[1])
            optimals.append(v[3])
            optimals.append(v[5])
        for i in range(len(optimals)):
            optimalsInt.append(int(optimals[i]))
        return optimalsInt

def average(list):
    return sum(list)/len(list)

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
            optimal = readOptimal(fpath)

    avgOfFirstFit = average(firstFitList)
    avgOfBestFit = average(bestFitList)
    avgOfWorstFit = average(worstFitList)

    print('\n')
    print('Maximum height of a bin: ', round(overload(x), 3))
    print('-----------------------------------------')
    print('FF:')
    print('\tAverage bin usage of First-Fit:', round(avgOfFirstFit, 3))
    print('\tAverage bin usage related to Best-Fit: ', (avgOfFirstFit/avgOfBestFit) * 100 - 100,'%')
    print('\tAverage bin usage related to Worst-Fit: ', (avgOfFirstFit/avgOfWorstFit) * 100 - 100,'%')
    print('\tMaximum item of First-Fit: ', max(firstFitList))
    print('\tMinimum item of First-Fit: ', min(firstFitList))
    print('-----------------------------------------')
    print('BF:')
    print('\tAverage bin usage of Best-Fit: ', round(avgOfBestFit, 3))
    print('\tAverage bin usage related to First-Fit: ', (avgOfBestFit/avgOfFirstFit) * 100 - 100,'%')
    print('\tAverage bin usage related to Worst-Fit: ', (avgOfBestFit/avgOfWorstFit) * 100 - 100,'%')
    print('\tMaximum item of Best-Fit: ', max(bestFitList))
    print('\tMinimum item of Best-Fit: ', min(bestFitList))
    print('-----------------------------------------')
    print('WF:')
    print('\tAverage bin usage of Worst-Fit: ', round(avgOfWorstFit,3))
    print('\tAverage bin usage related to First-Fit: ', (avgOfWorstFit/avgOfFirstFit) * 100 - 100,'%')
    print('\tAverage bin usage related to Best-Fit: ', (avgOfWorstFit/avgOfBestFit) * 100 - 100,'%')
    print('\tMaximum item of Worst-Fit: ', max(worstFitList))
    print('\tMinimum item of Worst-Fit: ', min(worstFitList))
    print('\n')


    fig, ax = plt.subplots()
    fig, ax.plot(optimal,'y', linewidth=0.5)
    ax.set_title('Optimals')
    plt.show()

    fig, ax = plt.subplots()
    fig, ax.plot(firstFitList,  'g', linewidth=0.5)
    ax.set_title('First-Fit algorithm')
    plt.show()

    fig, ax = plt.subplots()
    ax.plot(bestFitList,  'r--', linewidth=0.5)
    ax.set_title('Best-Fit algorithm')
    plt.show()

    fig, ax = plt.subplots()
    ax.plot(worstFitList, 'b-', linewidth=0.5)
    ax.set_title('Worst-Fit algorithm')
    plt.show()

    fig, ax = plt.subplots()
    ax.plot(firstFitList, 'g',  bestFitList, 'r--', worstFitList, 'b-', optimal,'y', linewidth=0.5)
    ax.set_title('Summarized')
    plt.show()
    print('i printed sum')


for x in range(1, 5):
    temp = x
    if x == 2:
        temp = 1.65
        readDirectory(temp)
    elif x == 4:
        temp = 5
        readDirectory(temp)
    else:
        readDirectory(temp)