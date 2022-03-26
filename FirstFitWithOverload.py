import sys
import os

path = r"D:\Thesis\thesis\input_bison"  # nem működik input_bison-nal
os.chdir(path)

cost = 2


def overload(c):
    if (0 <= c) and (c <= 3 / 2):
        s = 1 + sys.maxsize

    elif (3 / 2 <= c) and (c <= 9 / 5):
        s = 1 + 1 / c
        print('overload')

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
            break
    # print(bins)
    return bins


def firstFit(overloadCost, data):
    usedBins = 1
    maxHeight = overload(overloadCost)
    remainingSpace = []
    remainingSpace.append(maxHeight)

    for i in range(len(data)):
        usedBins = firstFitForOneItem(usedBins, remainingSpace, data[i], maxHeight)

    return usedBins - 1


def read_text(fpath):
    with open(fpath, 'r') as f:
        f.readline()
        data = f.readlines()
        dataInt = []
        for i in range(len(data)):
            dataInt.append(int(data[i]))
        result = firstFit(cost, dataInt)
        print(result)


for file in os.listdir():
    if file.endswith('.BPP'):
        fpath = f"{path}\{file}"
        read_text(fpath)

# print("Használt ládák száma: ", firstFit([1, 0.9, 0.8, 0.7, 0.6, 0.5, 0.4, 0.3, 0.2, 0.1], 10, 2))

# h: rekeszek száma
# wi: i-edik rekesznek a magassága (a benne lévő dobozok összemagassága)
# si: i-edik rekesznek a max magassága (ameddig pakolhatjuk a ládákat)
# pi: i-edik doboznak a magassága
# dj: j-edik rekesznek a fennmaradó része (ha oda raknánk be az i-edik dobozt)
# k: eredmény (result)
