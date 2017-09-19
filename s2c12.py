from w4rumutils import *
from binascii import *
import string

shitKey = b'B\xd3V\x1e\xff\xff\xb4\xa2G\x8d\x1f\xa7\xfbm\x03\\'
def aesRandomEncryptWeirdMode(plain):
    key = shitKey 
    suffix = a2b_base64('Um9sbGluJyBpbiBteSA1LjAKV2l0aCBteSByYWctdG9wIGRvd24gc28gbXkgaGFpciBjYW4gYmxvdwpUaGUgZ2lybGllcyBvbiBzdGFuZGJ5IHdhdmluZyBqdXN0IHRvIHNheSBoaQpEaWQgeW91IHN0b3A/IE5vLCBJIGp1c3QgZHJvdmUgYnkK')
    plain = plain + suffix
    return aesEcbEncrypt(plain, key)

print(ecbCrack(aesRandomEncryptWeirdMode, 16).decode())
