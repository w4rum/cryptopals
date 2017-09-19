from w4rumutils import *
from binascii import *

crypt = open('6.txt', 'r').read()#.replace('\n', '')
crypt = a2b_base64(crypt)[:-1]
#print(crypt)
#crypt = unhexlify('1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736')

print(vigenereCrack(crypt, keysizeTolerance=1)[0][0].decode())
#print(transposeBlocks([b'AAAAA', b'BBBBB', b'CCCCC', b'DDD']))
#print(transposeBlocks(stripeBytes(b'12345678901234567890', 3)))
