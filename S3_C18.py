# Implement CTR, the stream cipher mode

import base64
from S2_C10 import xor, encrypt_aes_ecb

string = base64.b64decode("L77na/nrFsKvynd6HzOoG7GHTLXsTVu9qvY/2syLXzhPweyyMTJULu/6/kXX0KSvoOLSFQ==")

def ctr_stream_generate(nonce, length):
    stream = b""
    for i in range(length // 16 + (0 if length % 16 == 0 else 1)):
        stream += nonce.to_bytes(8, byteorder='little') + i.to_bytes(8, byteorder='little')
    return stream

def ctr_encrypt_decrypt(string, key, nonce: int):
    length = len(string)
    stream = ctr_stream_generate(nonce, length)
    plaintext = xor(string, encrypt_aes_ecb(stream, key))
    return plaintext

if __name__ == "__main__":
    print(ctr_encrypt_decrypt(string, b"YELLOW SUBMARINE", 0).decode("utf-8"))