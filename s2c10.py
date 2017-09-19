from w4rumutils import *

key = b'YELLOW SUBMARINE'
iv = b'\x00'*16

crypt = open('10.txt', 'r').read()
crypt = a2b_base64(crypt).rstrip()

print(aesCbcDecrypt(crypt, key, iv))
