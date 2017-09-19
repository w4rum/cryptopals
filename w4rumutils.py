from binascii import *
from scipy import spatial
from Crypto.Cipher import AES
from math import *
from random import *
import functools
import string
import struct
import os

def hex2b64(h):
    return b2a_base64(unhexlify(h))[:-1].decode()

def xor(b, mask):
    b = bytearray(b)
    for i in range(0, len(b)):
        b[i] = b[i] ^ mask[i % len(mask)]

    return bytes(b)

def hammingDist(b1, b2):
    diff = 0
    for i in range(0, min(len(b1), len(b2))):
            byteXor = (b1[i] ^ b2[i])
            for j in range(0,8):
                diff += (byteXor >> j) & 1

    diff += abs(len(b1) - len(b2)) * 8
    return diff

def scoreEnglish(b):
    # unigram frequency of english texts, alphabetical order
    freq = [0] * 256
    freq[ord('a')] = 	0.08167
    freq[ord('b')] = 	0.01492
    freq[ord('c')] = 	0.02782
    freq[ord('d')] = 	0.04253
    freq[ord('e')] = 	0.12702
    freq[ord('f')] = 	0.02228
    freq[ord('g')] = 	0.02015
    freq[ord('h')] = 	0.06094
    freq[ord('i')] = 	0.06966
    freq[ord('j')] = 	0.00153
    freq[ord('k')] = 	0.00772
    freq[ord('l')] = 	0.04025
    freq[ord('m')] = 	0.02406
    freq[ord('n')] = 	0.06749
    freq[ord('o')] = 	0.07507
    freq[ord('p')] = 	0.01929
    freq[ord('q')] = 	0.00095
    freq[ord('r')] = 	0.05987
    freq[ord('s')] = 	0.06327
    freq[ord('t')] = 	0.09056
    freq[ord('u')] = 	0.02758
    freq[ord('v')] = 	0.00978
    freq[ord('w')] = 	0.02360
    freq[ord('x')] = 	0.00150
    freq[ord('y')] = 	0.01974
    freq[ord('z')] = 	0.00074
    freq[ord(' ')] =    0.23200

    freqCur = [0] * 256

    # count unigram occurrences
    for c in b:
        c = chr(c).lower()
        freqCur[ord(c)] += 1

    # convert to relative amounts
    size = 0
    for i in range(0, len(freqCur)):
        size += freqCur[i]

    for i in range(0, len(freqCur)):
        freqCur[i] = freqCur[i] / size

    # calculate cosine similarity to normal frequency
    # see https://stackoverflow.com/questions/15710292/how-to-compute-letter-frequency-similarity
    # and https://stackoverflow.com/questions/18424228/cosine-similarity-between-2-number-lists#18424933
    score = 1 - spatial.distance.cosine(freq, freqCur)

    return score

def singleXorCrack(crypt):
    highscore = -1
    best = ''
    bestKey = -1
    for i in range(0,256):
        cur = xor(crypt, bytes([i]))
        curScore = scoreEnglish(cur)
        if curScore > highscore:
            highscore = curScore
            best = cur
            bestKey = i
    return [best, bestKey, highscore]

def vigenereCrack(crypt, keysizeMax=40, keysizeTolerance=4):
    #print(hexlify(crypt))
    keysizes = vigenereFindKeysizes(crypt, keysizeMax, keysizeTolerance)
    #keysizes= [x for x in range(28,40)]
    results = []
    for ks in keysizes:
        blocks = stripeBytes(crypt, ks)
        tr = transposeBlocks(blocks)
        key = []
        for b in tr:
            crackRes = singleXorCrack(b)
            #print('%d, %f, %s' % (crackRes[1], crackRes[2], crackRes[0]))
            key.append(crackRes[1])
        #print('KS %d: %s' % (ks, functools.reduce(lambda x, y: x + chr(y), key, '')))
        results.append([xor(crypt, key), key])
    #print(xor(crypt, b'X'))
    return results 
        

def vigenereFindKeysizes(crypt, keysizeMax, keysizeTolerance, chunksToConsider=10):
    # find probable keysizes
    # by taking average hamming distance over first 10 (default) blocks of brute-forced
    # size
    keysizes = []
    for i in range (2, keysizeMax):
        dist = 0
        chunkCount = min(chunksToConsider, len(crypt) // i - 1)
        for j in range(chunkCount):
            # add distances between each two neighboring blocks
            dist += hammingDist(crypt[j*i:(j+1)*i], crypt[(j+1)*i:(j+2)*i])
        dist /= chunkCount
        dist /= i
        keysizes.append([i, dist])
    keysizes = sorted(keysizes, key=lambda x:x[1])[:keysizeTolerance]
    return [x[0] for x in keysizes]
 
def stripeBytes(b, stripeSize):
    return [b[i:i+stripeSize] for i in range(0, len(b), stripeSize)]

def transposeBlocks(blocks):
    tr = [bytearray() for x in range(len(blocks[0]))]
    for i in range(len(blocks)):
        for j in range(len(blocks[i])):
            tr[j].append(blocks[i][j])

    return [bytes(x) for x in tr]

def aesEcbDecrypt(crypt, key):
    assert len(crypt) % 16 == 0
    cfg = AES.new(key, AES.MODE_ECB)
    return cfg.decrypt(crypt)

def aesEcbEncrypt(plain, key):
    assert len(plain) % 16 == 0
    cfg = AES.new(key, AES.MODE_ECB)
    return cfg.encrypt(plain)

def aesCbcEncrypt(plain, key, iv):
    assert len(plain) % 16 == 0
    prevCrypt = iv
    crypt = bytearray()
    blocks = stripeBytes(plain, 16)
    for b in blocks:
        curCrypt = aesEcbEncrypt(xor(b, prevCrypt), key)
        prevCrypt = curCrypt
        crypt.extend(curCrypt)
    return bytes(crypt)

def aesCbcDecrypt(crypt, key, iv):
    assert len(crypt) % 16 == 0
    prevCrypt = iv
    plain = bytearray()
    blocks = stripeBytes(crypt, 16)
    for b in blocks:
        curPlain = xor(aesEcbDecrypt(b, key), prevCrypt)
        prevCrypt = b
        plain.extend(curPlain)
    return bytes(plain)

def pad(b, size):
    padSize = size - len(b) % size
    if padSize == size:
        return b + bytes([size]) * size
    else:
        return b + bytes([padSize]) * padSize

def unpad(b, size=16):
    last = b[len(b) - size:]
    padsize = ord(last[-1:])
    if padsize > 0 and padsize <= size:
        # check if actually is padding
        for i in range(0, padsize):
            if ord(last[size-1-i:size-1-i+1]) != padsize:
                raise ValueError('incorrect padding!')
        last = last[:size-padsize]
        return b[:-size] + last
    else:
        raise ValueError('incorrect padding!')

def aesRandomEncrypt(plain):
    key = os.urandom(16) 
    prefix = os.urandom(randint(5,10))
    suffix = os.urandom(randint(5,10))
    plain = prefix + plain + suffix
    if randint(0,1) == 1:
        print('ECB')
        return aesEcbEncrypt(plain, key)
    else:
        print('CBC')
        iv = os.urandom(16)
        return aesCbcEncrypt(plain, key, iv)

def detectEcb(crypt):
    blocks = stripeBytes(crypt, 16)
    s = set()
    for b in blocks:
        s.add(b)
    distinct = len(s)
    actual = ceil(len(crypt) / 16)
    if distinct < actual:
        return True
    else:
        return False
        #print('%d/%d distinct blocks!' % (distinct, actual))

def buildDict(func, pre, known, block, blocksize, blockOffset=0):
    d = dict()
    offset = blocksize*blockOffset
    for c in range(256):
        c = chr(c)
        plain = pre + known + c.encode()
        #print(plain)
        crypt = func(plain)[offset:offset+blocksize*block-1]
        #print(crypt)
        d.update({crypt: c})
    return d

def ecbCrack(func, blocksize=16, blockOffset=0):
    blockCount = ceil(len(func(b'')) / blocksize) - blockOffset
    #print('blockCount='+str(blockCount))
    offset = blocksize*blockOffset
    known = bytearray()
    for bl in range(1, blockCount+1):
        for i in range(1, blocksize+1):
            pre = b'A'*(blocksize-i)
            d = buildDict(func, pre, known, bl, blocksize, blockOffset)
            #print(d)
            #return
            crypt = func(pre)
            #print(crypt)
            try:
                newChar = d[crypt[offset:offset+blocksize*bl-1]]
            except KeyError:
                return bytes(known)
            #print(newChar)
            known.extend(newChar.encode())
            #print(known)

def parseUserString(s):
    attr = [x.split('=') for x in s.split('&')]
    return attr

def toUserString(user):
    return '&'.join(['%s=%s' % (k, v) for k, v in user])

def genUser(email):
    email = email.replace('&','').replace('=','')
    user = [
            ['email', email],
            ['uid', 10],
            ['role', 'user']]
    return user

def profile_for(email):
    user = genUser(email)
    return toUserString(user)

userEncKey = b'\x0f \x93\x12\xcf\x043\xd5_-\x9c\x1e\x03\xafJ\x84'
def encUser(userString):
    return aesEcbEncrypt(userString.encode(), userEncKey)

def decUser(cryptUserString):
    return parseUserString(aesEcbDecrypt(cryptUserString, userEncKey).decode())

def bitflip(src, target, known):
    #print('src=' + hexlify(src).decode())
    #print('tar=' + hexlify(target).decode())
    #print('kwn=' + known.__str__())
    assert len(src) == len(target) == len(known)
    diff = xor(target, known)
    return xor(src, diff)

def paddingOracle(oracle, crypt, iv, blocksize=16):
    blocks = [iv]
    blocks.extend(stripeBytes(crypt, blocksize))
    known = [b''] * (len(blocks) - 1)
    for i in reversed(range(1, len(blocks)-0)):
        for ic in range(blocksize):
            #print(len(blocks))
            #print(len(crypt))
            #input('')
            #print('known=')
            #print(known)
            for guess in range(256):
                #if guess == 1:
                #    continue
                curBlock = blocks[i]
                prevBlock = blocks[i-1]
                #print('i=' + str(i))
                #print('ic=' + str(ic))
                #print('curBlock=' + hexlify(curBlock).decode())
                #print('crypt=' + hexlify(crypt).decode())
                #print('guess=' + hex(guess))
                target = curBlock[:blocksize-1-ic] + bytes([ic+1]) * (ic+1)
                knownBlock = curBlock[:blocksize-1-ic] + bytes([guess]) + known[i-1]
                moddedBlock = bitflip(prevBlock, target, knownBlock)
                if oracle(b''.join([moddedBlock, curBlock])) and not (guess == 1 and ic == 0):
                    known[i-1] = bytes([guess]) + known[i-1]
                    #print("RIGHT")
                    break
                #else:
                    #print("WRONG")
    return b''.join(known)
