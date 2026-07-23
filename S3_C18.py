# Implement CTR, the stream cipher mode

import base64
from S2_C10 import xor, encrypt_aes_ecb

string = base64.b64decode("L77na/nrFsKvynd6HzOoG7GHTLXsTVu9qvY/2syLXzhPweyyMTJULu/6/kXX0KSvoOLSFQ==")

def encrypt_decrypt_ctr(string, key, nonce: int):
    plaintext = b""
    for i in range(0, len(string)//16 + (1 if len(string) % 16 != 0 else 0)):
        keystream = encrypt_aes_ecb(nonce.to_bytes(8, byteorder='little') + i.to_bytes(8, byteorder='little'), key)
        plaintext += xor(string[i*16:(i+1)*16], keystream)
    return plaintext

if __name__ == "__main__":
    print(encrypt_decrypt_ctr(string, b"YELLOW SUBMARINE", 0).decode("utf-8"))