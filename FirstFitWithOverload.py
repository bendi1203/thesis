import sys

def overload(c):
    if((0 <= c) and (c <= 3/2)):
        c = sys.maxsize
    elif((3/2 <= c) and (c <= 9/5)):
        c = 1/c
    elif((9/5 <= c) and (c <= 14/3)):
        c = 2/(3 * c)
    else:
        c = 1/(3 * c)
