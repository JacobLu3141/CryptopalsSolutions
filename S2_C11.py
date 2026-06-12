# An ECB/CBC detection oracle

import random
from S2_C10 import encrypt_aes_ecb_padding, encrypt_aes_cbc

def key_generate(n):
    key = random.randbytes(n)
    return key

def aes_key_generate():
    key = key_generate(16)
    return key

def encryption_oracle(plaintext):
    n1 = random.randint(5, 10)
    n2 = random.randint(5, 10)
    b1 = key_generate(n1)
    b2 = key_generate(n2)
    plaintext = b1 + plaintext + b2
    key = aes_key_generate()
    IV = aes_key_generate()
    cbc = random.choice([True, False])
    if cbc:
        return encrypt_aes_cbc(plaintext, key, IV)
    else:
        return encrypt_aes_ecb_padding(plaintext, key)

# for testing
def encryption_oracle_with_answer(plaintext):
    n1 = random.randint(5, 10)
    n2 = random.randint(5, 10)
    b1 = key_generate(n1)
    b2 = key_generate(n2)
    plaintext = b1 + plaintext + b2
    key = aes_key_generate()
    IV = aes_key_generate()
    cbc = random.choice([True, False])
    if cbc:
        return ["cbc", encrypt_aes_cbc(plaintext, key, IV)]
    else:
        return ["ecb", encrypt_aes_ecb_padding(plaintext, key)]

def encryption_detection_oracle():
    ciphertext = encryption_oracle("ABCDEFGHIJKLMNOPABCDEFGHIJKLMNOPABCDEFGHIJKLMNOP".encode('utf-8'))
    ciphertext = ciphertext
    my_guess = ciphertext[16:32] == ciphertext[32:48]
    return(my_guess)

# for testing
def encryption_detection_oracle():
    mode_ciphertext = encryption_oracle_with_answer("ABCDEFGHIJKLMNOPABCDEFGHIJKLMNOPABCDEFGHIJKLMNOP".encode('utf-8'))
    correct_answer = mode_ciphertext[0]
    ciphertext = mode_ciphertext[1]
    my_guess = ciphertext[16:32] == ciphertext[32:48]
    return(my_guess == correct_answer)

if __name__ == "__main__":
    works = True
    for i in range(100000):
        if not (encryption_detection_oracle()[1]):
            works = False
            print(i)
    print(works)