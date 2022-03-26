import sys
import os

# c-t ide megadni
# firstfitet egyesével az elemekre meghívni
path = r"D:\Thesis\thesis\input_bison"  # nem működik input_bison-nal
os.chdir(path)


#   törlendő
def read_text(fpath):
    with open(fpath, 'r') as f:
        print(f.read())


#   törlendő

for file in os.listdir():
    if file.endswith('.BPP'):
        fpath = f"{path}\{file}"
        read_text(fpath)  # törlendő
        print('---')  # törlendő


def overload(c):
    if (0 <= c) and (c <= 3 / 2):
        s = 1 + sys.maxsize
        return s

    elif (3 / 2 <= c) and (c <= 9 / 5):
        s = 1 + 1 / c
        return s

    elif (9 / 5 <= c) and (c <= 14 / 3):
        s = 1 + 2 / (3 * c)
        return s

    else:
        s = 1 + 1 / (3 * c)
        return s


def firstfit(items, numberOfItems, overloadCost):
    usedBins = 0
    maxHeight = overload(overloadCost)

    remainingSpace = [0] * numberOfItems

    for i in range(numberOfItems):
        j = 0
        while j < usedBins:
            if remainingSpace[j] >= items[i]:
                remainingSpace[j] -= items[i]
                break
            j += 1

        if j == usedBins:
            remainingSpace[usedBins] = maxHeight - items[j]
            usedBins += 1
    return usedBins


print("Használt ládák száma: ", firstfit([1, 0.9, 0.8, 0.7, 0.6, 0.5, 0.4, 0.3, 0.2, 0.1], 10, 2))

# h: rekeszek száma
# wi: i-edik rekesznek a magassága (a benne lévő dobozok összemagassága)
# si: i-edik rekesznek a max magassága (ameddig pakolhatjuk a ládákat)
# pi: i-edik doboznak a magassága
# dj: j-edik rekesznek a fennmaradó része (ha oda raknánk be az i-edik dobozt)
# k: eredmény (result)