# Convert hex to base64

import base64

def hex_to_base64(hex_string):
    raw_string = bytes.fromhex(hex_string)
    base64_string = base64.encodebytes(raw_string)
    return base64_string.decode("utf-8")

hex_string = "49276d206b696c6c696e6720796f757220627261696e206c696b65206120706f69736f6e6f7573206d757368726f6f6d"

print(hex_to_base64(hex_string))