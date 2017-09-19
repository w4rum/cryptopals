from w4rumutils import *

crypt = unhexlify('1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736')

highscore = 0
best = ''
xors = []
for i in range(0,256):
    xors.append([i, xor(crypt, bytes([i]))])

for s in sorted(xors, key=lambda x:scoreEnglish(x[1]), reverse=True)[0:10]:
    print('%d: %s' % (s[0], s[1]))
