from w4rumutils import *
from random import *
from binascii import *

key = b'\xb4}\r)\xf5\xb2J\xce\xe3\xcf\x17X\x05\x94\xad6'
iv  = b'5\x19\x18\xff\xa4\xc7Gb\x8cN#8\x1d\x1c\x8b\xfa'

def encShit(i):
    strings = ["MDAwMDAwTm93IHRoYXQgdGhlIHBhcnR5IGlzIGp1bXBpbmc=",
    "MDAwMDAxV2l0aCB0aGUgYmFzcyBraWNrZWQgaW4gYW5kIHRoZSBWZWdhJ3MgYXJlIHB1bXBpbic=",
    "MDAwMDAyUXVpY2sgdG8gdGhlIHBvaW50LCB0byB0aGUgcG9pbnQsIG5vIGZha2luZw==",
    "MDAwMDAzQ29va2luZyBNQydzIGxpa2UgYSBwb3VuZCBvZiBiYWNvbg==",
    "MDAwMDA0QnVybmluZyAnZW0sIGlmIHlvdSBhaW4ndCBxdWljayBhbmQgbmltYmxl",
    "MDAwMDA1SSBnbyBjcmF6eSB3aGVuIEkgaGVhciBhIGN5bWJhbA==",
    "MDAwMDA2QW5kIGEgaGlnaCBoYXQgd2l0aCBhIHNvdXBlZCB1cCB0ZW1wbw==",
    "MDAwMDA3SSdtIG9uIGEgcm9sbCwgaXQncyB0aW1lIHRvIGdvIHNvbG8=",
    "MDAwMDA4b2xsaW4nIGluIG15IGZpdmUgcG9pbnQgb2g=",
    "MDAwMDA5aXRoIG15IHJhZy10b3AgZG93biBzbyBteSBoYWlyIGNhbiBibG93"]
    #s = a2b_base64(strings[randint(0,9)])
    s = a2b_base64(strings[i])
    return aesCbcEncrypt(pad(s, 16), key, iv)

def decShit(b):
    try:
        res = unpad(aesCbcDecrypt(b, key, iv), 16)
        #print(res)
        return True
    except ValueError:
        return False

#                       x              x               x
#                       1234567890123456789012345678901234567
#aesCbcEncrypt(pad(b'hello this is my super secret message', 16), key, iv)
#crypt = crypt[:30] + b'\xff' + crypt[31:]
#print(aesCbcDecrypt(crypt, key, iv))
for i in range(10):
    crypt = encShit(i)
    print(unpad(paddingOracle(decShit, crypt , iv)))
