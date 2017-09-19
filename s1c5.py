from w4rumutils import *

raw = b"Burning 'em, if you ain't quick and nimble\nI go crazy when I hear a cymbal"
print(hexlify(xor(raw, b'ICE')))
