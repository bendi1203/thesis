import sys

def overload(c):
    if((0 <= c) and (c <= 3/2)):
        c = 1 + sys.maxsize
    elif((3/2 <= c) and (c <= 9/5)):
        c = 1 + 1/c
    elif((9/5 <= c) and (c <= 14/3)):
        c = 1 + 2/(3 * c)
    else:
        c = 1 + 1/(3 * c)