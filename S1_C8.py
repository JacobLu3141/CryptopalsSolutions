# Detect AES in ECB mode

def logic():
    with open('Data\\S1_C8.txt', 'r') as file:
        lineNum = 0
        correctLine = 0
        while True:
            newline = file.readline()
            if newline:
                lineNum += 1
                seen = []
                for i in range(len(newline)//32):
                    new_string = newline[32*i:32*(i+1)]
                    if new_string in seen:
                        # print(lineNum, "sus")
                        correctLine = newline
                    else:
                        seen.append(new_string)
            else:
                break
        print(correctLine.strip())

if __name__ == "__main__":
    logic()