from w4rumutils import *
from binascii import *

crypt = a2b_base64('L77na/nrFsKvynd6HzOoG7GHTLXsTVu9qvY/2syLXzhPweyyMTJULu/6/kXX0KSvoOLSFQ==')
plain = b'chello dis iz gud mesuje'
key = b'YELLOW SUBMARINE'
print(aesCtr(crypt, key))
print(aesCtr(aesCtr(plain, key), key)) 
