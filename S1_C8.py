# Detect AES in ECB mode

def logic():
    with open('Cryptopals\S1_C8.txt', 'r') as file:
        lineNum = 0
        while True:
            newline = file.readline()
            if newline:
                lineNum += 1
                seen = []
                for i in range(len(newline)//32):
                    new_string = newline[32*i:32*(i+1)]
                    if new_string in seen:
                        print(lineNum, "sus")
                    else:
                        seen.append(new_string)
            else:
                break

if __name__ == "__main__":
    print("d880619740a8a19b7840a8a31c810a3d08649af70dc06f4fd5d2d69c744cd283e2dd052f6b641dbf9d11b0348542bb5708649af70dc06f4fd5d2d69c744cd2839475c9dfdbc1d46597949d9c7e82bf5a08649af70dc06f4fd5d2d69c744cd28397a93eab8d6aecd566489154789a6b0308649af70dc06f4fd5d2d69c744cd283d403180c98c8f6db1f2a3f9c4040deb0ab51b29933f2c123c58386b06fba186a")