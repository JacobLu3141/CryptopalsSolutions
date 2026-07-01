# Single-byte XOR cipher

from S1_C2 import hexor

def hex_to_word(hex_string, xor):
    word = ""
    for i in range(len(hex_string)//2):
        ascii = int(hexor(hex_string[i*2:i*2+2], xor), 16)
        word += chr(ascii)
    return word

hex_string = "1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736"

if __name__ == "__main__":
    print(hex_to_word(hex_string, "58"))

# Notice that 78 is the odd one out; the rest are in the form 1_ or 3_, which could represent uppercase and lowercase letters, respectively. It therefore makes sense that 78 is a space.
# Or you could just run a Caesar cipher from 0 to 127 lmao