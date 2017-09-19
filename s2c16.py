from w4rumutils import *

def buildInput(s):
    prefix = b"comment1=cooking%20MCs;userdata="
    suffix = b";comment2=%20like%20a%20pound%20of%20bacon"
    s = s.replace(b';',b'').replace(b'=',b'')
    return prefix + s + suffix

key = b"\x1d\xea\r\x9a\r\x02'\x0eN\xa7\x82\xf5[\xf3AU"
iv  = b'\x8f9y\x06\xfeN\xa8B\xfe\x08\xb8U\x7f\xb0\xae\x89'
def encryptShit(s):
    plain = buildInput(s)
    return aesCbcEncrypt(plain, key, iv)

def decryptAndLook(b):
    dec = aesCbcDecrypt(b, key, iv)
    return [b";admin=true;" in dec, dec]

payload = b'A'*16
crypt = encryptShit(payload)
cryptsnippet = crypt[2*16:3*16]
mod = bitflip(cryptsnippet, b';admin=true;0lik', b';comment2=%20lik')
#mod = bitflip(cryptsnippet, b';comment3=%20lik', b';comment2=%20lik')
#print(mod)
crypt = crypt[:2*16] + mod + crypt[3*16:]
res = decryptAndLook(crypt)
print(res)
#print(stripeBytes(res[1], 16))

