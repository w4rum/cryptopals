from w4rumutils import *
from datetime import *

r = MT19937(int.from_bytes('shitfuckshitshit'.encode(), byteorder='big'))
#r = MT19937(round(datetime.now().timestamp()))
#print(round(datetime.now().timestamp()))
for i in range(20):
    print('%d: %d' % (i, r.extract_number()))
