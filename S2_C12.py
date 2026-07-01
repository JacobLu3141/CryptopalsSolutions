# Byte-at-a-time ECB decryption (Simple)

import base64, random
from S2_C9 import pad
from S2_C10 import encrypt_aes_ecb, encrypt_aes_ecb_padding
from S2_C11 import aes_key_generate

random.seed(42)
KEY = aes_key_generate()

appended_string = "Um9sbGluJyBpbiBteSA1LjAKV2l0aCBteSByYWctdG9wIGRvd24gc28gbXkgaGFpciBjYW4gYmxvdwpUaGUgZ2lybGllcyBvbiBzdGFuZGJ5IHdhdmluZyBqdXN0IHRvIHNheSBoaQpEaWQgeW91IHN0b3A/IE5vLCBJIGp1c3QgZHJvdmUgYnkK"
appended_bytes = base64.b64decode(appended_string)
    
def encrypt_aes_ecb_global_append(plaintext):
    return encrypt_aes_ecb(plaintext + appended_bytes, KEY)

def encrypt_aes_ecb_global_append_pad(plaintext):
    return encrypt_aes_ecb(pad(plaintext + appended_bytes, 16), KEY)

# slightly illegal but the intended way of finding block length is trivial anyways
# I'm just too lazy to change it; NEVER use the unpadded version of the oracle outside of verifying stuff we already know
def block_length():
    for i in range(40):
        try:
            print(encrypt_aes_ecb_global_append(("A" * (i + 1)).encode('utf-8')))
            print(i+1) # reaches here in cycles of 16, so block size is 16
            # at i = 38, we have two copies of "AAAAAAAAAAAAAAAA"
            # to verify deterministic encryption between plaintext and key
        except:
            print("not", i+1)

def ecb_decode():
    message = b''
    appended_bytes_copy = appended_bytes
    for i in range(len(appended_bytes_copy)):
        first_ciphertext = encrypt_aes_ecb_global_append_pad(("A" * 15).encode('utf-8') + appended_bytes_copy)[0:16]
        for j in range(128):
            if encrypt_aes_ecb_global_append_pad(("A" * 15).encode('utf-8') + bytes([j]))[0:16] == first_ciphertext:
                message += bytes([j])
                break
        appended_bytes_copy = appended_bytes_copy[1:]
    return message

if __name__ == "__main__":
    print(ecb_decode())