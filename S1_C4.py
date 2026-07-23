# Detect single-character XOR

from S1_C3 import hex_to_word

def logic():
    with open('Data\S1_C4.txt', 'r') as file:
        for line in file:
            first = True
            seen = []
            for c in line:
                if first and not c in seen:
                    print(c,end="")
                    print(c,end="")
                    seen.append(c)
                first = not first
            if (len(seen)) <= 6:
                print(line)
            
print(hex_to_word("7b5a4215415d544115415d5015455447414c155c46155f4058455c5b523f", hex(53)[2:]))

# Iterate through each line, finding the number of distinct hex digits among the sixteens digits of each character
# Find that only one string has 5 or fewer distinct hex digits
# Find a character that is repeated regularly (in this case 15)
# Find the XOR that turns it into a space (20)