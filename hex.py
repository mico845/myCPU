import os

dirname = os.path.dirname(os.path.abspath(__file__))


with open(os.path.join(dirname, 'display.bin'), 'wb') as f:
    for var in range(256):
        var = str(var)
        var = int(var, base=16)
        byte = var.to_bytes(2, byteorder= 'little')
        f.write(byte)