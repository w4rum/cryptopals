# mt19937 coefficients
w = 32
n = 624
m = 397
r = 31
a = 0x9908B0DF
u = 11
d = 0xFFFFFFFF
s = 7
b = 0x9D2C5680
t = 15
c = 0xEFC60000
l = 18
f = 1812433253

def wLowBits(x):
    return ((1 << w) - 1) & x

def untamper(y):
    y = inverseRightShiftXor(y, l)
    y = inverseLeftShiftBitmaskXor(y, t, c)
    y = inverseLeftShiftBitmaskXor(y, s, b)
    y = inverseRightShiftXor(y, u)
    return y

def tamper(y):
    y = y ^ (y >> u)
    # omitted d(0xffff ffff)-mask since it does nothing as y
    # will always be an unsigned 32-bit int at the start of the
    # process anyways
    y = y ^ ((y << s) & b)
    y = y ^ ((y << t) & c)
    y = y ^ (y >> l)
    return y

class MT19937:
    lower_mask = (1 << r) - 1
    upper_mask = wLowBits(~lower_mask)

    def __init__(self, seed):
        self.mt = [0] * n
        self.index = n
        self.mt[0] = seed
        for i in range (1, n):
            self.mt[i] = wLowBits(f * (self.mt[i-1] ^ (self.mt[i-1] >> (w-2))) + i)

    def setState(self, vals, index):
        assert len(vals) == n
        assert 0 <= index <= n
        for i in range(len(vals)):
            self.mt[i] = vals[i]
        self.index = index

    def extract_number(self):
        if self.index >= n:
            self.twist()

        y = self.mt[self.index]
        y = tamper(y)

        self.index += 1
        return wLowBits(y)

    def twist(self):
        for i in range(n):
            x = (self.mt[i] & MT19937.upper_mask) + (self.mt[(i+1) % n] & MT19937.lower_mask)
            xA = x >> 1
            if (x % 2) != 0:
                xA = xA ^ a
            self.mt[i] = self.mt[(i+m) % n] ^ xA
        self.index = 0

def inverseRightShiftXor(x, shift):
    # How it works:
    #  (The operators on the left show was has been done to reach the value next to it)
    #
    #orig 10110111010111100111111001110010
    #          >> 11 10110111010111100111111001110010
    #   ^ 10110111010010001001010110111101
    #     First 11 bits are still the same
    #      => We can reconstruct the 2nd 11 bits
    #          >> 11 10110111010010001001010110111101 >>> 11
    #             m: 111111111110000000000 (partMask (1<<(11+1)-1) << (32-11*2))
    #             &  101101110100000000000
    #     10110111010111100111110110111101
    #     Second 11 bits reconstructed
    #      => We can reconstruct the 3rd 11 bits (only 10 left at this point)
    #          >> 11 10110111010111100111110110111101
    #             m: 000000000001111111111 (partMask (1<<(11+1)-1) << (32-11*3))
    #                                      (rightshift on negative)
    #             &  000000000001111001111
    #   ^ 10110111010111100111111001110010
    #     Done!
    partIndex = 1
    while (partIndex * shift < w):
        partMask = (1 << shift) - 1
        partMaskShift = w - shift*(partIndex+1)
        if partMaskShift > 0:
            partMask = partMask << partMaskShift
        else:
            partMask = partMask >> -partMaskShift

        part = (x >> shift) & partMask
        x ^= part
        partIndex += 1
    return x

def inverseLeftShiftBitmaskXor(x, shift, mask):
    # same method as inverseRightShiftXor but with a mask for the part
    partIndex = 1
    while (partIndex * shift < w):
        partMask = (1 << shift) - 1
        partMaskShift = shift*(partIndex)
        partMask <<= partMaskShift

        part = (x << shift) & partMask & mask
        x ^= part
        partIndex += 1
    return x


