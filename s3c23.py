from w4rumutils import *

r = MT19937(0x796f75726172726976616c6973666f72747569746f7573)
r2 = MT19937(0)

n = 624
vals = [0] * n
for i in range(n):
    vals[i] = untamper(r.extract_number())

r2.setState(vals, 0)
for i in range(n):
    r2.extract_number()

for i in range(100):
    print('Index: %d' % i)
    print('R : %d' % r.extract_number())
    print('R2: %d' % r2.extract_number())
