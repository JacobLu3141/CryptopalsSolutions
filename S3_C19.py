# Break fixed-nonce CTR mode using substitutions

import base64, random
from S2_C10 import xor
from S3_C18 import encrypt_decrypt_ctr

random.seed(42)
KEY = random.randbytes(16)

ciphertexts = []
over_32_bytes = []

with open("Data\\S3_C19.txt") as file:
    ciphertexts = list(map(lambda line: encrypt_decrypt_ctr(base64.b64decode(line.strip()), KEY, 0), file.readlines()))

for i in range(len(ciphertexts)):
    if len(ciphertexts[i]) >= 32:
        over_32_bytes.append(i)

c1, c2, c3 = tuple(ciphertexts[i] for i in over_32_bytes[:3])
d1 = ciphertexts[over_32_bytes[0]] + b"  "
d4 = ciphertexts[over_32_bytes[3]] + b"    "
d6 = ciphertexts[over_32_bytes[5]]

one_two = xor(c1, c2)
one_three = xor(c1, c3)
two_three = xor(c2, c3)
one_four = xor(d1, d4)
one_six = xor(d1, d6)
four_six = xor(d4, d6)

# I brute forced the entire string of 32 bytes by xor'ing three plaintexts 
# against each other and guessing the most probable characters at any point
def retrieve_32_bytes():
    print(xor(one_two,   b" " * 0 + b"I have passed with a nod of the ")) # 1
    print(xor(one_two,   b" " * 0 + b"Or have lingered awhile and said")) # 2
    print()
    print(xor(one_three, b" " * 0 + b"I have passed with a nod of the ")) # 1
    print(xor(one_three, b" " * 0 + b"This other his helper and friend")) # 3
    print()
    print(xor(two_three, b" " * 0 + b"Or have lingered awhile and said")) # 2
    print(xor(two_three, b" " * 0 + b"This other his helper and friend")) # 3

# I figured out the last 6 bytes in the same way, with different strings
def retrieve_38_bytes():
    print(xor(one_six,   b"I have passed with a nod of the head  ")) # 1
    print(xor(one_six,   b"He, too, has been changed in his turn,")) # 6

    print(xor(one_four,  b"I have passed with a nod of the head  ")) # 1
    print(xor(one_four,  b"He might have won fame in the end,    ")) # 4

    print(xor(four_six,  b"He might have won fame in the end,    ")) # 4
    print(xor(four_six,  b"He, too, has been changed in his turn,")) # 6

if __name__ == "__main__":
    for i in range(len(ciphertexts)):
        print(xor(xor(ciphertexts[i], ciphertexts[over_32_bytes[5]]), b"He, too, has been changed in his turn,").decode('utf-8'))