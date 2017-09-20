from w4rumutils import *

def randomCrypt(plain, key):
    r = MT19937(key & 0xff)
    crypt = bytearray()
    
    for b in plain:
        keystream = r.extract_number() & 0xf
        crypt.append(b ^ keystream)

    return bytes(crypt)

seed = 0x47455420544f20544845204348415041274149
plain = b'chelo dis neis taxt'
crypt = randomCrypt(plain, seed)
print(plain)
print(crypt)
print(randomCrypt(crypt, seed))
