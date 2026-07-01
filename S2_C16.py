# CBC bitflipping attacks

import random
from S2_C10 import xor, encrypt_aes_cbc, decrypt_aes_cbc
from S2_C11 import aes_key_generate

random.seed(42)
KEY = aes_key_generate()

def quote(s):
    out = bytearray()
    for b in s:
        if b == ord(';'):
            out.extend(b'\\;')
        elif b == ord('='):
            out.extend(b'\\=')
        else:
            out.append(b)
    return bytes(out)

def encrypt_aes_cbc_prepend_append(plaintext):
    prepend = "comment1=cooking%20MCs;userdata=".encode()
    append = ";comment2=%20like%20a%20pound%20of%20bacon".encode()
    middle = quote(plaintext)
    ciphertext = encrypt_aes_cbc(prepend + middle + append, KEY, bytes([0]) * 16)
    return ciphertext

def string_exists(ciphertext):
    plaintext = decrypt_aes_cbc(ciphertext, KEY, bytes([0]) * 16)
    return plaintext.find(";admin=true;".encode()) > -1

def attack():
    ciphertext = encrypt_aes_cbc_prepend_append("jacob:admin<true".encode())
    # print(ciphertext)
    ciphertext = ciphertext[:21] + bytes([ciphertext[21] ^ 1]) + ciphertext[22:27] + bytes([ciphertext[27] ^ 1]) + ciphertext[28:]
    # print(ciphertext)
    print(string_exists(ciphertext))
    
if __name__ == "__main__":
    attack()