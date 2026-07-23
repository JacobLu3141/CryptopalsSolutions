# The CBC padding oracle

import random, base64
from S2_C10 import encrypt_aes_cbc, decrypt_aes_cbc

seeded_random = random.Random()
seeded_random.seed(42)
KEY = seeded_random.randbytes(16)

def select():
    IV = random.randbytes(16)
    with open("S3_C17.txt") as file:
        strings = list(map(lambda line: base64.b64decode(line.strip()), file.readlines()))
        selected = random.choice(strings)
        ciphertext = encrypt_aes_cbc(selected, KEY, IV)
        return ciphertext, IV

def padding(ciphertext, IV):
    try:
        plaintext = decrypt_aes_cbc(ciphertext, KEY, IV)
        return True
    except:
        return False

# find P_n given C_{n-1} || C_n
def attack(ciphertext, IV):
    plaintext = b""
    end_bytes = b""
    # one byte at a time
    for i in range(1, 17):
        plaintext_byte = []
        for j in range(256):
            trial_bytes = ciphertext[:-(16+i)] + bytes([j]) + end_bytes + ciphertext[-16:]
            if padding(trial_bytes, IV):
                plaintext_byte.append(j)
        # even if padding works, we don't know that the last byte is b'\x01'
        # flip the second last byte to confirm
        if (i == 1):
            for j in plaintext_byte:
                test_bytes = ciphertext[:-(i+17)] + bytes([ciphertext[-(i+17)] ^ 1]) + bytes([j]) + end_bytes + ciphertext[-16:]
                if padding(test_bytes, IV):
                    correct_byte = j
                else:
                    pass
        else:
            correct_byte = plaintext_byte[0]
        prepend = bytes([correct_byte ^ i ^ ciphertext[-(i+16)]])
        plaintext = prepend + plaintext
        end_bytes = bytes([correct_byte]) + end_bytes
        end_bytes = bytes([b ^ i ^ (i + 1) for b in end_bytes])
    return plaintext

if __name__ == "__main__":
    ciphertext, IV = select()
    ciphertext = IV + ciphertext
    plaintext = b""
    for i in range(len(ciphertext) // 16 - 1):
        plaintext += attack(ciphertext[16*i:16*(i+2)], IV)
    print(plaintext)

'''
d(c) = p
d(j) = i
d(c ^ j) = c ^ i
d(c) = c ^ i ^ j
'''