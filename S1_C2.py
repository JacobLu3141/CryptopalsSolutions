# Fixed XOR

def hexor(hex1, hex2):
    thing = hex(int(hex1, 16) ^ int(hex2, 16))[2:]
    if (len(thing) == 1):
        thing = "0" + thing
    return thing

s1 = "1c0111001f010100061a024b53535009181c"
s2 = "686974207468652062756c6c277320657965"

if __name__ == "__main__":
    print(hexor(s1, s2))