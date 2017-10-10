from w4rumutils import *
from random import *

def edit(crypt, key, offset, newText):
    plain = aesCtr(crypt, key)
    newPlain = bytearray()
    newPlain = plain[:offset] + newText
    newPlain += plain[len(newPlain):]
    newCrypt = aesCtr(newPlain, key)
    return bytes(newCrypt)

plain = b'THIS IS A SUPER SECRET TEXT PLEASE DO NOT DECRYPT WITHOUT EQUALLY SECRET KEY'
secretKey = bytes([randint(0,255) for x in range(32)])
crypt = aesCtr(plain, secretKey)

def editAttacker(crypt, offset, newText):
    return edit(crypt, secretKey, offset, newText)

inj = b'A' * len(crypt)
injOffset = 0
edited = editAttacker(crypt, injOffset, inj)
# At this point we have two ciphertexts produced
# by XORing two plaintexts with the same key
#     p1 ^ k = c1
#     p2 ^ k = c2
# =>  p1 ^ k ^ p2 ^ k = c1 ^ c2
# =>  p1 ^ p2 = c1 ^ c2
# =>  p1 = c1 ^ c2 ^ p2
recovPlain = xor(xor(crypt, edited), inj)
print("[---] Original plaintext:")
print(plain)
print("[---] Original ciphertext:")
print(crypt)
print("[---] Our ciphertext:")
print(edited)
print("[---] Recovered plaintext:")
print(recovPlain)

