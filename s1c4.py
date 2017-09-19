from w4rumutils import *

bests = []
with open('4.txt', 'r') as f:
    for line in f:
        line = unhexlify(line.rstrip())
        bests.append(singleXorCrack(line))

for s in sorted(bests, key=lambda x:x[2], reverse=True)[0:10]:
    print('Score %f (Key %d): %s' % (s[2], s[1], s[0]))
