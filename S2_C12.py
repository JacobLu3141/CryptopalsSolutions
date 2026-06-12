import base64
from Crypto.Util.Padding import pad
from S2_C10 import encrypt_aes_ecb, encrypt_aes_ecb_padding

KEY = b'5\x157l\xcd4t]\x85\x91\xd3\xfa\x0e\xa4\xf4\x8f'
appended_string = "Um9sbGluJyBpbiBteSA1LjAKV2l0aCBteSByYWctdG9wIGRvd24gc28gbXkgaGFpciBjYW4gYmxvdwpUaGUgZ2lybGllcyBvbiBzdGFuZGJ5IHdhdmluZyBqdXN0IHRvIHNheSBoaQpEaWQgeW91IHN0b3A/IE5vLCBJIGp1c3QgZHJvdmUgYnkK"
appended_bytes = base64.b64decode(appended_string)
    
def encrypt_aes_ecb_global_append(plaintext):
    return encrypt_aes_ecb(plaintext + appended_bytes, KEY)

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
        first_ciphertext = encrypt_aes_ecb_padding(("A" * 15).encode('utf-8') + appended_bytes_copy, KEY)[0:16]
        for j in range(128):
            if encrypt_aes_ecb_padding(("A" * 15).encode('utf-8') + bytes([j]), KEY)[0:16] == first_ciphertext:
                message += bytes([j])
                break
        appended_bytes_copy = appended_bytes_copy[1:]
    return message

if __name__ == "__main__":
    print(ecb_decode())