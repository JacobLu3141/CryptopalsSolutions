# Implement repeating-key XOR

from S1_C2 import hexor

# repeated hexor
def repexor(hex1, rep):
    string = ""
    acc = 0
    charNum = 0
    while (acc < len(hex1)):
        string += hexor(hex1[acc:acc+2], rep[charNum:charNum+2])
        acc += 2
        charNum = (charNum+2) % len(rep)
    return string

string1 = "Burning 'em, if you ain't quick and nimble I go crazy when I hear a cymbal"

if __name__ == "__main__":
    print(repexor(string1.encode().hex(), "ICE".encode().hex()))