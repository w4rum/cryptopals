from w4rumutils import *

def randomCrypt(plain, key):
    r = MT19937(key & 0xffff)
    crypt = bytearray()
    
    for b in plain:
        keystream = r.extract_number() & 0xff
        crypt.append(b ^ keystream)

    return bytes(crypt)

plain = b'A'*14
pre = b''.join([bytes([randint(0,255)]) for x in range(randint(1, 100))])
plain = pre + plain
secretKey = randint(0,2**16)
crypt = randomCrypt(plain, secretKey)
c = 0
for i in range(2**16):
    # only print every 100 steps
    if c % 100 == 0:
        print("Trying seed " + hex(i))
        c = 0
    c += 1
    testCrypt = randomCrypt(plain, i)
    if crypt == testCrypt:
        print("Secret key was " + hex(i))
        print("(Confirmation: " + hex(secretKey) + ")")
        print("Plain:")
        print(plain)
        print("Encrypted:")
        print(crypt)
        break

