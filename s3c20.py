from w4rumutils import *
from binascii import *
import sys

plain = []
with open('20.txt', 'r') as f:
    plain = [a2b_base64(line[:-1]) for line in f] 
key = b'\xcb\n\x98\xbbC\xd7\xec\x9aR\xde,\xf6\x93\x8d3\xf5'
crypt = [aesCtr(x, key) for x in plain]

# truncate to same size
smallestLength = -1
for c in crypt:
    if smallestLength == -1 or len(c) < smallestLength:
        smallestLength = len(c)
crypt = [x[:smallestLength] for x in crypt]

res = vigenereCrack(b''.join(crypt), keysizes=[smallestLength])[0]
print('Key: ' + hexlify(bytes(res[1])).decode())
for s in stripeBytes(res[0], smallestLength):
    print(s.decode())
