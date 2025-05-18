import os
import pin
import assembly as ASM

dirname = os.path.dirname(__file__)
filename = os.path.join(dirname, 'micro.bin')

micro = [pin.HALT for _ in range(0x10000)]

def complie_addr2(addr, ir, psw, index):
    global micro
    op = ir & 0xf0
    amd = (ir >> 2) & 0x3
    ams = ir & 0x3
    INST = ASM.INSTRUCTIONS[2]
    if op not in INST:
        micro[addr] = pin.CYC
        return
    
    am = (amd, ams)

    if am not in INST[op]:
        micro[addr] = pin.CYC
        return
    
    EXEC = INST[op][am]
    if index < len(EXEC):
        micro[addr] = EXEC[index]
    else:
        micro[addr] = pin.CYC
    

def complie_addr1(addr, ir, psw, index):
    pass
def complie_addr0(addr, ir, psw, index):
    global micro

    op = ir

    INST = ASM.INSTRUCTIONS[0]
    if op not in INST:
        micro[addr] = pin.CYC
        return

    EXEC = INST[op]
    if index < len(EXEC):
        micro[addr] = EXEC[index]
    else:
        micro[addr] = pin.CYC



for addr in range(0x10000):
    # addr = ir(8) | psw(4) | cyc(4)
    ir = addr >> 8
    psw = (addr >> 4) & 0xf
    cyc = addr &0xf

    if cyc < len(ASM.FETCH):
        micro[addr] = ASM.FETCH[cyc]
        continue

    addr2 = ir & (1 << 7)
    addr1 = ir & (1 << 6)

    index = cyc - len(ASM.FETCH)
    
    if addr2:
        complie_addr2(addr, ir, psw, index)
    elif addr1:
        complie_addr1(addr, ir, psw, index)
    else:
        complie_addr0(addr, ir, psw, index)

with open(filename, 'wb') as file:
    for var in micro:
        value = var.to_bytes(4, byteorder='little')
        file.write(value)

print(f"Microcode written to {filename}")
