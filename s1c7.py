from w4rumutils import *

crypt = open('7.txt', 'r').read()
crypt = a2b_base64(crypt)
key = "YELLOW SUBMARINE"

print(aesEcbDecrypt(crypt, key))
