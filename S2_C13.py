# ECB cut-and-paste

import random
from S2_C10 import encrypt_aes_ecb_padding
from S1_C7 import decrypt_aes_ecb_unpadding
from S2_C11 import aes_key_generate

random.seed(42)
KEY = aes_key_generate()

def parse(query):
    word = ""
    key = ""
    hash = {}
    for char in query:
        if char == '=':
            key = word
            word = ""
        elif char == '&':
            hash[key] = word
            key = ""
            word = ""
        else:
            word += char
    hash[key] = word
    return hash

def profile_for(email):
    uid = 10
    for char in email:
        if char in ['&', '=']:
            raise ValueError("Invalid email.")
    code = "email=" + email + "&uid=" + str(uid) + "&role=user"
    return code

def encrypt_profile(email):
    return encrypt_aes_ecb_padding(profile_for(email).encode('utf-8'), KEY)

def decrypt_profile(ciphertext):
    return parse(decrypt_aes_ecb_unpadding(ciphertext, KEY).decode('utf-8'))
        
if __name__ == "__main__":
    main_bytes = encrypt_profile("foooo@bar.com") # add extra characters to make the code "email=...&role=" exactly 32 characters long
    s1 = main_bytes[0:32]
    admin_bytes = encrypt_profile("meowmeow12admin\x0b\x0b\x0b\x0b\x0b\x0b\x0b\x0b\x0b\x0b\x0b") # pad until 16 characters
    s2 = admin_bytes[16:32]
    print(decrypt_profile(s1+s2))