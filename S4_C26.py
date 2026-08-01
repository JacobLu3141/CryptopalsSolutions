# CTR bitflipping

import random
from S3_C18 import ctr_encrypt_decrypt
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
    ciphertext = ctr_encrypt_decrypt(prepend + middle + append, KEY, 0)
    return ciphertext

def string_exists(ciphertext):
    plaintext = ctr_encrypt_decrypt(ciphertext, KEY, 0)
    return plaintext.find(";admin=true;".encode()) > -1

# change the ';' and '=' characters to bitflip later
def main():
    ciphertext = encrypt_aes_cbc_prepend_append("jacob:admin<true".encode())
    # shift everything by one block since CTR bitflipping 
    # affects the current plaintext rather than the next plaintext
    ciphertext = ciphertext[:37] + bytes([ciphertext[37] ^ 1]) + ciphertext[38:43] + bytes([ciphertext[43] ^ 1]) + ciphertext[44:]
    print(string_exists(ciphertext))
    
if __name__ == "__main__":
    main()