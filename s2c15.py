from w4rumutils import *

print(unpad(b'ICE ICE BABY\x04\x04\x04\x04'))
try:
    print(unpad(b'ICE ICE BABY\x05\x05\x05\x05'))
except ValueError:
    print('no')
try:
    print(unpad(b'ICE ICE BABY\x01\x02\x03\x04'))
except ValueError:
    print('no')
