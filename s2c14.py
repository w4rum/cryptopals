from w4rumutils import *
from binascii import *
import sys
import string


def aesRandomEncryptHardMode(plain):
    # random key
    key = b'=\x96\xaa\xec\xea\xd4QC\x85y\x9d\xa0<\x97\xa0\x1d'
    randomprefix = b"a3 \x19\xdb4\xb06\xadxU\xcfz\xdby\x19\xf8q\x1a\xb0\xc1p\xb4-\xde\xef\xef\xe0h~\xcd\xceo\xf5\x89\xe4\xce\x8f\xa6 \xf4a\x15\xf6\x02\xf0\x1c7\xed\x90e\xf5\x8a\xeb\xcf\xdc\x90\xc2z\x9e\x1c'\x0f\x93 \x8b\xcb\xe9\x8d.\x87\xa5\x1c\x0b\xb55\xce\x15\x8d\x04\xce\x0c\x1a\xb2\x1f\x95\xaf\x87\xa8O:&|\xc4w/4"
    target = a2b_base64('Um9sbGluJyBpbiBteSA1LjAKV2l0aCBteSByYWctdG9wIGRvd24gc28gbXkgaGFpciBjYW4gYmxvdwpUaGUgZ2lybGllcyBvbiBzdGFuZGJ5IHdhdmluZyBqdXN0IHRvIHNheSBoaQpEaWQgeW91IHN0b3A/IE5vLCBJIGp1c3QgZHJvdmUgYnkK')
    plain = randomprefix + plain + target
    return aesEcbEncrypt(plain, key)

# need 31 'A' bytes to get pure 'A' block
# => prefix is 15 bytes short
# block amount changes when 15+7 'A's are added
# => suffix is 6 bytes short
def usePayload(payload):
    return aesRandomEncryptHardMode(b'A'*15 + payload)

# pure 'A' block appears on index 7 (8th block)
# => prefix, padded with 15 bytes, is 7 blocks long
print(ecbCrack(usePayload, blockOffset=7))

'''
payload = 'A'*15+'A'*16
#print('in')
#print(sys.argv[1].encode())
crypt = aesRandomEncryptHardMode(payload.encode())
cryptblocks = [crypt[i:i+16] for i in range(0,len(crypt), 16)]

for i, val in enumerate(cryptblocks):
    if i > 3 and i < 12:
        print('%i: %s' % (i, val))

print('Length: ' + str(len(crypt)))
'''
