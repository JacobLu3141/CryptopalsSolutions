# PKCS#7 padding validation

def unpad(string, block_size):
    if len(string) % block_size != 0:
        raise ValueError("invalid padding")
    if string[-1] < 1 or string[-1] > block_size:
        raise ValueError("invalid padding")
    amount_of_padding = string[-1]
    for i in range(amount_of_padding):
        if (string[-1] == amount_of_padding):
            string = string[0:-1]
        else:
            raise ValueError("invalid padding")
    return string

if __name__ == "__main__":
    try:
        print(unpad(b"ICE ICE BABY\x04\x04\x04\x04"))
    except Exception as e:
        print(e)
    try:
        print(unpad(b"ICE ICE BABY\x05\x05\x05\x05"))
    except Exception as e:
        print(e)
    try:
        print(unpad(b"ICE ICE BABY\x01\x02\x03\x04"))
    except Exception as e:
        print(e)
    try:
        print(unpad(b"ICE ICE BABY\x04\x03\x02\x01"))
    except Exception as e:
        print(e)