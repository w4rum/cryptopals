from w4rumutils import *
import string
import sys

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

# email=... 6 symbols, 10 symbols short to full block
email  = 'A'*10
# payload on own block
#email += pad(b'admin', 16).decode()
# &uid= ... 17 symbols, 15 symbols short last block
email += 'A'*15
# push 'user' into last block
email += 'A'*4

us = profile_for(email)
crypt = encUser(us)

# cut off 'user' block
crypt = crypt[:-16]
# 'admin' [+padding] encrypted
crypt += b'M{\xa3\xca\x9e\xa5\x0e\xe1\xe2\xe3\xbdr\x0f\x00\x89R'

plain = decUser(crypt)
print('Input: ' + email)
print('Length of ciphertext: ' + str(len(crypt)))
print('Cipher:')
print([crypt[i:i+16] for i in range(0, len(crypt), 16)])
print('Result:')
print(plain)
#print(unpad(b'BBBBBBBBBBBBBBBBAAAAAAAAAAAAAAAA', 16))
