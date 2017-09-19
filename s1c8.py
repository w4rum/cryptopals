from w4rumutils import *
from math import *

with open('8.txt', 'r') as f:
    i = 0
    for line in f:
        line = unhexlify(line.rstrip())
        blocks = stripeBytes(line, 16)
        s = set()
        for b in blocks:
            s.add(b)
        distinct = len(s)
        actual = ceil(len(line) / 16)
        if distinct < actual:
            print('Entry #%d has only %d/%d distinct blocks!' % (i, distinct, actual))
        i += 1

