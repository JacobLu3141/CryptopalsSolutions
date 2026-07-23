# Implement PKCS#7 padding

def pad(b, length):
    add = length - (len(b) % length)
    b += bytes([add]) * add
    return b

if __name__ == "__main__":
    thing = pad("YELLOW SUBMARINE".encode('utf-8'), 20)
    print(thing)