import sys

def overload(c):
    if((0 <= c) and (c <= 3/2)):
        s = 1 + sys.maxsize
        return s

    elif((3/2 <= c) and (c <= 9/5)):
        s = 1 + 1/c
        return s

    elif((9/5 <= c) and (c <= 14/3)):
        s = 1 + 2/(3 * c)
        return s

    else:
        s = 1 + 1/(3 * c)
        return s

def firstfit(items, n, c):   #   p: elemek súlya, n : elemek darabszáma, c túltöltési költség
        h = 0   # felhasznált ládák száma
        s = overload(c)  # láda magassága túltöltéssel
        d = [0] * n

        for i in range(n): #  végigmegy az elemeken
            j = 0
            while j < h: #  végigmegy a ládákon
                if d[j] >= items[i]:
                    print('if-ben d[j]: ', d[j], 'if-ben p[j]: ', items[j])
                    d[j] -= items[i]
                    break
                j += 1

            if (j == h): #  végigmegy és nem rakja bele egyikbe sem
                d[h] = s - items[j]
                h += 1
        return h

print("Használt ládák száma: ",firstfit([1, 0.9, 0.8, 0.7, 0.6, 0.5, 0.4, 0.3, 0.2, 0.1], 10, 2))