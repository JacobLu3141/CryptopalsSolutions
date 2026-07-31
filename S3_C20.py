# Break fixed-nonce CTR statistically

import base64, random
from S1_C6 import shiftCandidate
from S2_C10 import encrypt_aes_ecb, xor, repxor
from S3_C18 import ctr_stream_generate, ctr_encrypt_decrypt

random.seed(42)
KEY = random.randbytes(16)

if __name__ == "__main__":
    ciphertexts = []
    over_32_bytes = []
    # same logic as in S1_C6, without having to compute Hamming distance
    with open("Data\\S3_C20.txt") as file:
        ciphertexts = list(map(lambda line: ctr_encrypt_decrypt(base64.b64decode(line.strip()), KEY, 0), file.readlines()))
        block_length = min(len(c) for c in ciphertexts)
        stream = ctr_stream_generate(0, block_length)
        concat = b''.join(c[:block_length] for c in ciphertexts)
        keystream_copy = b""
        for i in range(block_length):
            ciphertext_string = b''.join(c[i:i+1] for c in ciphertexts)
            keystream_copy += bytes.fromhex(shiftCandidate(ciphertext_string.hex()))
        # turns out upon running, our space finder isn't perfectly accurate
        # so we make tweaks based on context
        # e.g. "5=iday -> Friday"
        keystream = b""
        keystream += xor(bytes([keystream_copy[0]]), xor(b'5', b'F'))
        keystream += xor(bytes([keystream_copy[1]]), xor(b'=', b'r'))
        keystream += keystream_copy[2:19]
        keystream += xor(bytes([keystream_copy[19]]), xor(b')', b'l'))
        keystream += xor(bytes([keystream_copy[20]]), xor(b'&', b'c'))
        keystream += xor(bytes([keystream_copy[21]]), xor(b'*', b'o'))
        keystream += keystream_copy[22:50]
        keystream += xor(bytes([keystream_copy[50]]), xor(b'e', b' '))
        keystream += keystream_copy[51:53]
        string = repxor(concat, keystream)
        for i in range(len(string) // 53):
            print(string[53*i:53*(i+1)].decode('utf-8'))