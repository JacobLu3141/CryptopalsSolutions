# Break "random access read/write" AES CTR

import random, base64
from S1_C6 import getCode
from S1_C7 import decrypt_aes_ecb_unpadding
from S2_C10 import xor
from S3_C18 import ctr_encrypt_decrypt

random.seed(42)
KEY = random.randbytes(16)

def edit(ciphertext, offset, newtext):
    new_ciphertext = ctr_encrypt_decrypt(newtext, KEY, 0)
    edited = ciphertext[:offset] + new_ciphertext + ciphertext[offset + len(new_ciphertext):]
    return edited

# finally adopted the practice of having main() function
def main():
    with open("Data\\S1_C7.txt") as file:
        ciphertext = ctr_encrypt_decrypt(decrypt_aes_ecb_unpadding(base64.b64decode(getCode('Data\\S1_C7.txt')), b"YELLOW SUBMARINE"), KEY, 0)
        # print(len(plaintext)) # length is 2880
        LENGTH = 2880
        keystream = edit(ciphertext, 0, b"\x00" * LENGTH)
        print(xor(keystream, ciphertext))
        
if __name__ == "__main__":
    main()