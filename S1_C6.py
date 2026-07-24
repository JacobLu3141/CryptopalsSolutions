# Break repeating-key XOR

import base64
from S1_C2 import hexor
from S1_C5 import repexor

def hamming(hex1, hex2):
    xor = hexor(hex1, hex2)
    bor = bin(int(xor, 16))[2:]
    ham = 0
    for i in bor:
        if i == '1':
            ham += 1
    return ham

def spaceCandidate(block):
    seen = {}
    max = 0
    maxChar = block[0:2]
    for i in range(len(block)//2):
        char = block[2*i:2*(i+1)]
        if char not in seen:
            seen[char] = 1
        else:
            seen[char] += 1
            if seen[char] > max:
                max = seen[char]
                maxChar = char
    return maxChar

def shiftCandidate(block):
    return hexor(spaceCandidate(block), "20")

def getCode(fileName):
    with open(fileName, 'r') as file:
        cat = ""
        while True:
            newline = file.readline().strip() 
            if newline:
                cat += newline
            else:
                break
    return cat
        
if __name__ == "__main__":
    hexCat = base64.b64decode(getCode('Data\\S1_C6.txt')).hex()
    for i in range(2, 100):
        sum = 0
        for j in range(2875//i):
            sum += hamming(hexCat[2*i*j:2*i*(j+1)], hexCat[2*i*(j+1):2*i*(j+2)])
        # print(sum/(2875//i*i))
        
    # based on distribution of average hamming, length is 29
    KEYSIZE = 29
    blocks = []
    key = ""
    for i in range(KEYSIZE):
        blocks.append("")
    for i in range(len(hexCat)//2):
        blocks[i%KEYSIZE] += hexCat[2*i:2*(i+1)]
    for i in range(KEYSIZE):
        key += shiftCandidate(blocks[i])

    print(bytes.fromhex(repexor(hexCat, key)).decode('utf-8'))