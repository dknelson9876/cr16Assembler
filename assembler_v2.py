import sys
import argparse

ops = {
    'AND':      ('0','1'),
    'ANDI':     ('1'),
    'OR':       ('0','2'),
    'ORI':      ('2'),
    'XOR':      ('0','3'),
    'XORI':     ('3'),

    'ADD':      ('0','5'),
    'ADDI':     ('5'),
    'ADDU':     ('0','6'),
    'ADDUI':    ('6'),
    'ADDC':     ('0','7'),
    'ADDCI':    ('7'),
    'MUL':      ('0','E'),
    'MULI':     ('E'),
    'SUB':      ('0','9'),
    'SUBI':     ('9'),
    'SUBC':     ('0','A'),
    'SUBCI':    ('A'),
    'CMP':      ('0','B'),
    'CMPI':     ('B'),

    'MOV':      ('0','D'),
    'MOVI':     ('D'),
    'LSH':      ('8','4'),
    'LSHI':     ('8',''), # duh.... come back to this
    'ASHU':     ('8','6'),
    'ASHUI':    ('8',''), # duh.... come back to this
    'LUI':      ('F'),
    'LOAD':     ('4','0'),
    'STOR':     ('4','4'),

    'BEQ':      ('C','0'),
    'BNE':      ('C','1'),
    'BCS':      ('C','2'),
    'BCC':      ('C','3'),
    'BHI':      ('C','4'),
    'BLS':      ('C','5'),
    'BGT':      ('C','6'),
    'BLE':      ('C','7'),
    'BFS':      ('C','8'),
    'BFC':      ('C','9'),
    'BLO':      ('C','A'),
    'BHS':      ('C','B'),
    'BLT':      ('C','C'),
    'BGE':      ('C','D'),
    'BUC':      ('C','E'),

    'JEQ':      ('4','0','C'),
    'JNE':      ('4','1','C'),
    'JCS':      ('4','2','C'),
    'JCC':      ('4','3','C'),
    'JHI':      ('4','4','C'),
    'JLS':      ('4','5','C'),
    'JGT':      ('4','6','C'),
    'JLE':      ('4','7','C'),
    'JFS':      ('4','8','C'),
    'JFC':      ('4','9','C'),
    'JLO':      ('4','A','C'),
    'JHS':      ('4','B','C'),
    'JLT':      ('4','C','C'),
    'JGE':      ('4','D','C'),
    'JUC':      ('4','E','C'),

    'SNXB':     ('4','4'),
    'ZRXB':     ('4','6'),
    'JAL':      ('4','8'),
    'TBIT':     ('4','A'),
    'TBITI':    ('4','E'),
    'LPR':      ('4','1'),
    'SPR':      ('4','5'),
    'DI':       ('4','0','3','0'),
    'EI':       ('4','0','7','0'),
    'EXCP':     ('4','0','B'),
    'RETX':     ('4','0','9','0'),

    'WAIT':     ('0','0','0','0'),
}

def encode():
    print("encode")

# ----------- BEGIN MAIN ---------------------
# parser = argparse.ArgumentParser(description='This is the Assembler')
# parser.add_argument('-f', dest='file')
# args = parser.parse_args()
# encode(args.file)
op_lens = [[],[],[],[]]
for key, val in ops.items():
    op_lens[len(val)-1].append(key)

for i, l in enumerate(op_lens):
    print(f"{i}: {l}")