# Implement CBC mode

import base64
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from S1_C6 import getCode
from S1_C7 import decrypt_aes_ecb

# why the hell did I not make this earlier
def xor(a, b):
    res = bytes(a1 ^ b1 for a1, b1 in zip(a, b))
    return res

def repxor(bytes, rep):
    string = b''
    for i in range(len(bytes)):
        string += xor(bytes[i], rep[i % len(rep)])
    return string

def encrypt_aes_ecb(plaintext, key):
    cipher = AES.new(key, AES.MODE_ECB)
    ciphertext = cipher.encrypt(plaintext)
    return ciphertext

def encrypt_aes_ecb_padding(plaintext, key):
    plaintext = pad(plaintext, 16)
    ciphertext = encrypt_aes_ecb(plaintext, key)
    return ciphertext

def encrypt_aes_ecb_yellow_sub(plaintext):
    return encrypt_aes_ecb(plaintext, "YELLOW SUBMARINE".encode('utf-8'))

def encrypt_aes_cbc(plaintext, key, IV):
    plaintext = pad(plaintext, 16)
    add = IV
    ciphertext = b''
    for i in range(len(plaintext) // 16):
        res = xor(add, plaintext[16*i:16*(i+1)])
        next_ciphertext = encrypt_aes_ecb(res, key)
        ciphertext += next_ciphertext
        add = next_ciphertext
    return ciphertext

def encrypt_aes_cbc_yellow_sub(plaintext):
    ciphertext = encrypt_aes_cbc(plaintext, "YELLOW SUBMARINE".encode('utf-8'), ('\x00' * 16).encode('utf-8'))
    return ciphertext

def decrypt_aes_cbc(ciphertext, key, IV):
    add = IV
    plaintext = b''
    for i in range(len(ciphertext) // 16):
        plaintext += xor(add, decrypt_aes_ecb(ciphertext[16*i:16*(i+1)], key))
        add = ciphertext[16*i:16*(i+1)]
    plaintext = unpad(plaintext, 16)
    return plaintext

def decrypt_aes_cbc_yellow_sub(ciphertext):
    plaintext = decrypt_aes_cbc(ciphertext, "YELLOW SUBMARINE".encode('utf-8'), ('\x00' * 16).encode('utf-8'))
    return plaintext

if __name__ == "__main__":
    b64 = getCode('Cryptopals\S2_C10.txt')
    text = base64.b64decode(b64)
    print(decrypt_aes_cbc_yellow_sub(text).decode('utf-8'))
    print(encrypt_aes_cbc_yellow_sub(decrypt_aes_cbc_yellow_sub(text)) == text)

'''
m = m1 + m2 + m3

encrypt:
c1 = enc(iv ^ m1)
c2 = enc(c1 ^ m2)
c3 = enc(c2 ^ m3)

decrypt:
m1 = iv ^ dec(c1)
m2 = c1 ^ dec(c2)
m3 = c2 ^ dec(c3)
'''

# holy shit this was implementation and debugging hell
# I will be shamelessly using chatgpt to debug errors from now on