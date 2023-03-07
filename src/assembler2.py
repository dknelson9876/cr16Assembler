import sys
import argparse


def read_stdin() -> list[str]:
    lines = []
    while True:
        line = input()
        if line == '':
            return lines
        lines.append(line)

class Assembler():
    def __init__(self, do_print_file: bool = False):
        self.do_print_file = do_print_file
    
    labels: dict[str, int] = {}

    def LSHI(self, imm, rdst) -> str:
        if imm < 0:
            return f'8{rdst}1{imm:1X}'
        else:
            return f'8{rdst}0{imm:1X}'

    def ASHUI(self, imm, rdst) -> str:
        if imm < 0:
            return f'8{rdst}3{imm:1X}'
        else:
            return f'8{rdst}2{imm:1X}'

    # supported inst_types: RR, R8S, R8U, R5S, R4U, N, 4I
    opcode_table: dict[str, tuple] = {
        'ADD':   ('RR',  lambda rsrc, rdst: f'0{rdst}5{rsrc}'),
        'ADDI':  ('R8S', lambda imm,  rdst: f'5{rdst}{imm:02X}'),
        'ADDU':  ('RR',  lambda rsrc, rdst: f'0{rdst}6{rsrc}'),
        'ADDUI': ('R8S', lambda imm,  rdst: f'6{rdst}{imm:02X}'),
        'ADDC':  ('RR',  lambda rsrc, rdst: f'0{rdst}7{rsrc}'),
        'ADDCI': ('R8S', lambda imm,  rdst: f'7{rdst}{imm:02X}'),
        'MUL':   ('RR',  lambda rsrc, rdst: f'0{rdst}E{rsrc}'),
        'MULI':  ('R8S', lambda imm,  rdst: f'E{rdst}{imm:02X}'),
        'SUB':   ('RR',  lambda rsrc, rdst: f'0{rdst}9{rsrc}'),
        'SUBI':  ('R8S', lambda imm,  rdst: f'9{rdst}{imm:02X}'),
        'SUBC':  ('RR',  lambda rsrc, rdst: f'0{rdst}A{rsrc}'),
        'SUBCI': ('R8S', lambda imm,  rdst: f'A{rdst}{imm:02X}'),
        'CMP':   ('RR',  lambda rsrc, rdst: f'0{rdst}B{rsrc}'),
        'CMPI':  ('R8S', lambda imm,  rdst: f'B{rdst}{imm:02X}'),
        'AND':   ('RR',  lambda rsrc, rdst: f'0{rdst}1{rsrc}'),
        'ANDI':  ('R8U', lambda imm,  rdst: f'1{rdst}{imm:02X}'),
        'OR':    ('RR',  lambda rsrc, rdst: f'0{rdst}1{rsrc}'),
        'ORI':   ('R8U', lambda imm,  rdst: f'1{rdst}{imm:02X}'),
        'XOR':   ('RR',  lambda rsrc, rdst: f'0{rdst}2{rsrc}'),
        'XORI':  ('R8U', lambda imm,  rdst: f'2{rdst}{imm:02X}'),
        'MOV':   ('RR',  lambda rsrc, rdst: f'0{rdst}D{rsrc}'),
        'MOVI':  ('R8U', lambda imm,  rdst: f'D{rdst}{imm:02X}'),
        'LSH':   ('RR',  lambda ramount, rdst: f'8{rdst}4{ramount}'),
        'LSHI':  ('R5S', LSHI),
        'ASHU':  ('RR',  lambda ramount, rdst: f'8{rdst}6{ramount}'),
        'ASHUI': ('R5S', ASHUI),
        'LUI':   ('R8U', lambda imm, rdst: f'F{rdst}{imm:02X}'),
        'LOAD':  ('RR',  lambda rdst, raddr: f'4{rdst}0{raddr}'),
        'STOR':  ('RR',  lambda rsrc, raddr: f'4{rsrc}4{raddr}'),
        'SNXB':  ('RR',  lambda rsrc, rdst: f'4{rdst}2{rsrc}'),
        'ZRXB':  ('RR',  lambda rsrc, rdst: f'4{rdst}6{rsrc}'),
        'JAL':   ('RR',  lambda rlink, rtarget: f'4{rlink}8{rtarget}'),
        'TBIT':  ('RR',  lambda roffset, rsrc: f'4{rsrc}A{roffset}'),
        'TBITI': ('R4U', lambda imm, rsrc: f'4{rsrc}E{imm:1X}'),
        'LPR':   ('RR',  lambda rsrc, rproc: f'4{rsrc}1{rproc}'),
        'SPR':   ('RR',  lambda rproc, rdst: f'4{rproc}5{rdst}'),
        'DI':    ('N',   lambda: '4030'),
        'EI':    ('N',   lambda: '4070'),
        'EXCP':  ('4U',  lambda vector: f'40B{vector:1X}'),
        'RETX':  ('N',   lambda: '4090'),
        'WAIT':  ('N',   lambda: '0000')
    }

    reg_codes: dict[str, str] = {
        'r0': '0',
        'r1': '1',
        'r2': '2',
        'r3': '3',
        'r4': '4',
        'r5': '5',
        'r6': '6',
        'r7': '7',
        'r8': '8',
        'r9': '9',
        'r10': 'A',
        'r11': 'B',
        'r12': 'C',
        'r13': 'D',
        'rA': 'E',  # return address
        'rsp': 'F'  # stack pointer
    }

    output_dir = './'




    def as_print(self, s: str) -> None:
        if self.do_print_file:
            sys.exit('error: `as_print` file not implemented')
        else:
            print(s)

        
        
    def check_num_args(self, parts: list[str], expected_num: int, line_num: int) -> None:
        if  len(parts) != expected_num:
            sys.exit(f'Error: Inst {parts[0]} expects {expected_num} arguments, found {len(parts)} on line {line_num}')
            
    def check_registers_exist(self, regs: list[str], line_num: int) -> None:
        for r in regs:
            if r not in self.reg_codes:
                sys.exit(f'Error: Found invalid second register {r} on line {line_num}')
                
    def check_unsigned_range(self, imm: int, bits: int, line_num: int) -> None:
        if imm < 0 or imm > 2**bits:
            sys.exit(f'Error: found out of range imm {imm} for zero extended immediate on line {line_num}')
            
    def check_signed_range(self, imm: int, bits: int, line_num: int) -> None:
        # TODO: verify this works as expected
        if imm < -(2**(bits-1)) or imm >= 2**(bits-1):
            sys.exit(f'Error: found out of range imm {imm} for sign extended immediate on line {line_num}')


    def assemble(self, lines: list[str]) -> None:
        address = -1
        for line_num, x in enumerate(lines):
            line = x.split('#')[0]  # discard comment at end of line
            parts = line.split()
            inst = parts.pop(0).upper()
            if inst not in self.opcode_table:
                # TODO: Implement symbol table
                sys.exit('Error: symbol table not implemented')

            inst_type, func = self.opcode_table[inst]

            if inst_type == 'RR':
                self.check_num_args(parts, 2, line_num)
                self.check_registers_exist(parts, line_num)
                self.as_print(func(self.reg_codes[parts[0]], self.reg_codes[parts[1]])) # type: ignore
            elif inst_type == 'R8U':
                self.check_num_args(parts, 2, line_num)
                imm, r2 = parts
                if imm[0] != '$':
                    # TODO
                    sys.exit(f'Error: symbol table not implemented: bad imm {imm} on line {line_num}')
                parsed_imm = int(imm[1:])
                self.check_unsigned_range(parsed_imm, 8, line_num)
                self.check_registers_exist([r2], line_num)
                self.as_print(func(parsed_imm, self.reg_codes[r2])) # type: ignore
                
            elif inst_type == 'R8S':
                self.check_num_args(parts, 2, line_num)
                imm, r2 = parts
                if imm[0] != '$':
                    # TODO
                    sys.exit(f'Error: symbol table not implemented: bad imm {imm} on line {line_num}')
                parsed_imm = int(imm[1:])
                self.check_signed_range(parsed_imm, 8, line_num)
                self.check_registers_exist([r2], line_num)
                self.as_print(func(parsed_imm, self.reg_codes[r2])) # type: ignore
                
            elif inst_type == 'R5S':
                self.check_num_args(parts, 2, line_num)
                imm, r2 = parts
                if imm[0] != '$':
                    # TODO
                    sys.exit(f'Error: symbol table not implemented: bad imm {imm} on line {line_num}')
                parsed_imm = int(imm[1:])
                self.check_signed_range(parsed_imm, 5, line_num)
                self.check_registers_exist([r2], line_num)
                self.as_print(func(parsed_imm, self.reg_codes[r2])) # type: ignore
                
            elif inst_type == 'R4U':
                self.check_num_args(parts, 2, line_num)
                imm, r2 = parts
                if imm[0] != '$':
                    # TODO
                    sys.exit(f'Error: symbol table not implemented: bad imm {imm} on line {line_num}')
                parsed_imm = int(imm[1:])
                self.check_unsigned_range(parsed_imm, 4, line_num)
                self.check_registers_exist([r2], line_num)
                self.as_print(func(parsed_imm, self.reg_codes[r2])) # type: ignore
                
            elif inst_type == '4U':
                self.check_num_args(parts, 1, line_num)
                imm = parts[0]
                if imm[0] != '$':
                    # TODO
                    sys.exit(f'Error: symbol table not implemented: bad imm {imm} on line {line_num}')
                parsed_imm = int(imm[1:])
                self.check_unsigned_range(parsed_imm, 4, line_num)
                self.as_print(func(parsed_imm)) # type: ignore
                
            elif inst_type == 'N':
                self.check_num_args(parts, 0, line_num)
                self.as_print(func()) # type: ignore

            else:
                sys.exit(f'Error: unimplemented instruction type {inst_type} for \n'
                        +f'instruction {inst} on line {line_num}')


def main() -> None:
    parser = argparse.ArgumentParser(description='This is the CR16 Assembler V2')
    parser.add_argument('file', nargs='?', help='The asm file to assemble')
    parser.add_argument('-i', '--input', action='store_true',
                        help='Read asm from stdin instead of a file (Reads lines until double new line)')
    args = parser.parse_args()

    asm_input = read_stdin() if args.input else open(args.file).readlines()
    
    asmblr = Assembler()

    asmblr.assemble(asm_input)


if __name__ == '__main__': main()
