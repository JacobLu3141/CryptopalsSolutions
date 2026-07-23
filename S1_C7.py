import base64
from Crypto.Cipher import AES
from S2_C15 import unpad
from S1_C6 import getCode

def decrypt_aes_ecb(ciphertext, key):
    cipher = AES.new(key, AES.MODE_ECB)
    plaintext = cipher.decrypt(ciphertext)
    return plaintext

def decrypt_aes_ecb_unpadding(ciphertext, key):
    plaintext = unpad(decrypt_aes_ecb(ciphertext, key), 16)
    return plaintext

def decrypt_aes_ecb_yellow_sub(ciphertext):
    return decrypt_aes_ecb_unpadding(ciphertext, "YELLOW SUBMARINE".encode('utf-8'))

if __name__ == "__main__":
    print(decrypt_aes_ecb_yellow_sub(base64.b64decode(getCode('S1_C7.txt'))))