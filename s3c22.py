from w4rumutils import *
from datetime import *
from random import *
from time import *

starttime = datetime(2017,9,20,13,33,37)
firstwait = timedelta(seconds=randint(40,1000))
secondwait = timedelta(seconds=randint(40,1000))
endtime = starttime + firstwait + secondwait
r = MT19937(int((starttime + firstwait).timestamp()))
output = r.extract_number()

# build possible seeds:
m = {}
for i in range((endtime - starttime).seconds):
    s = (starttime + timedelta(seconds=i))
    r2 = MT19937(int(s.timestamp()))
    m.update({ r2.extract_number(): s })

if output not in m:
    print("Didn't work...")
else:
    print("Worked! Seed was:")
    print(m[output])
