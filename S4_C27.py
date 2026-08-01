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
    ciphertext = encrypt_aes_cbc(prepend + middle + append, KEY, KEY)
    return ciphertext

def decryption_oracle(ciphertext):
    return decrypt_aes_cbc(ciphertext, KEY, KEY)
    
def main():
    # i am innocent sender :)
    plaintext = b""
    ciphertext = encrypt_aes_cbc_prepend_append(plaintext)
    # i am evil attacker >:)
    new_ciphertext = ciphertext[:16] + bytes([0]) * 16 + ciphertext[:16] + ciphertext[48:]
    # i am innocent receiver :)
    new_plaintext = decryption_oracle(new_ciphertext)
    # i am evil attacker >:)
    key = xor(new_plaintext[:16], new_plaintext[32:48])
    print(key)
    print(key == KEY)
    
if __name__ == "__main__":
    main()