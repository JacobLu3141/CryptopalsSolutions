# Byte-at-a-time ECB decryption (Harder)

import base64, random
from S2_C9 import pad
from S2_C10 import encrypt_aes_ecb, encrypt_aes_ecb_padding
from S2_C11 import key_generate, aes_key_generate

random.seed(42)
KEY = aes_key_generate()

appended_string = "Um9sbGluJyBpbiBteSA1LjAKV2l0aCBteSByYWctdG9wIGRvd24gc28gbXkgaGFpciBjYW4gYmxvdwpUaGUgZ2lybGllcyBvbiBzdGFuZGJ5IHdhdmluZyBqdXN0IHRvIHNheSBoaQpEaWQgeW91IHN0b3A/IE5vLCBJIGp1c3QgZHJvdmUgYnkK"
appended_bytes = base64.b64decode(appended_string)
prepended_bytes = key_generate(random.randint(0, 128))
    
def encrypt_c12_prepend(plaintext):
    return encrypt_aes_ecb(prepended_bytes + plaintext + appended_bytes, KEY)

def encrypt_c12_prepend_pad(plaintext):
    return encrypt_aes_ecb_padding(prepended_bytes + plaintext + appended_bytes, KEY)

def block_length():
    for i in range(48):
        try:
            print(encrypt_c12_prepend(("A" * (i + 1)).encode('utf-8')))
            print(i+1) # reaches here in cycles of 16, so block size is 16
            # at i = 48, we have two copies of "AAAAAAAAAAAAAAAA"
            # to verify deterministic encryption between plaintext and key
        except:
            print("", end="")

def find_duplicates(ciphertext):
    for i in range(len(ciphertext) // 16 - 1):
        counter = 0
        for j in range(16):
            if (ciphertext[16 * i + j] == ciphertext[16 * i + j + 16]):
                counter += 1
            else:
                counter = 0
        if (counter == 16):
            return i
    return -1

def prepend_length():
    number_of_a = 47
    duplicates = True
    while duplicates:
        number_of_a -= 1
        ciphertext = encrypt_c12_prepend_pad(("A" * number_of_a).encode('utf-8'))
        if find_duplicates(ciphertext) == -1:
            duplicates = False
    mod_16 = 47 - number_of_a
    length = 16 * find_duplicates(encrypt_c12_prepend_pad(("A" * 47).encode('utf-8'))) - 16 + mod_16
    return length

def ecb_decode():
    message = b''
    appended_bytes_copy = appended_bytes
    prepend_len = prepend_length()
    more_prepend = (16 - prepend_len % 16) % 16
    start_index = prepend_len + more_prepend
    for i in range(len(appended_bytes_copy)):
        first_ciphertext = encrypt_c12_prepend_pad(("A" * (15 + more_prepend)).encode('utf-8') + appended_bytes_copy)[start_index:start_index+16]
        for j in range(128):
            if encrypt_c12_prepend_pad(("A" * (15 + more_prepend)).encode('utf-8') + bytes([j]))[start_index:start_index+16] == first_ciphertext:
                message += bytes([j])
                break
        appended_bytes_copy = appended_bytes_copy[1:]
    return message

if __name__ == "__main__":
    print(ecb_decode())