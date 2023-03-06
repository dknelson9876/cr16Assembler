import sys
import argparse

labels: dict[str,int] = {}

opcode_table: dict[str,tuple] = {
    'ADD': ('RR', lambda rsrc, rdst: f'0{rdst}5{rsrc}'),
    'ADDI': ('R8U', lambda imm, rdst: f'5{rdst}{imm:02X}'),
    'ADDU': ('RR', lambda rsrc, rdst: f'0{rdst}6{rsrc}'),
}

reg_codes : dict[str,str] = {
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
    'rA':  'E', # return address
    'rsp': 'F'  # stack pointer
}

do_print_file = False
output_dir = './'

def read_stdin() -> list[str]:
    lines = []
    while True:
        line = input()
        if line == '':
            return lines
        lines.append(line)

def as_print(s: str) -> None:
    global do_print_file
    if do_print_file:
        sys.exit('error: `as_print` file not implemented')
    else:
        print(s)

def assemble(lines: list[str]) -> None:
    
    address = -1
    for i, x in enumerate(lines):
        line = x.split('#')[0] # discard comment at end of line
        parts = line.split()
        inst = parts[0].upper()
        if inst not in opcode_table:
            # TODO: Implement symbol table
            sys.exit('Error: symbol table not implemented')
            
        
        inst_type, func = opcode_table[parts[0]]
        
        if inst_type == 'RR':
            if len(parts) != 3:
                sys.exit(f'Error: RR type inst {parts[0]} expects two arguments, found {len(parts)-1}')
            if parts[1] not in reg_codes:
                sys.exit(f'Error: Found invalid first register {parts[1]} on line {i}')
            if parts[2] not in reg_codes:
                sys.exit(f'Error: Found invalid second register {parts[2]} on line {i}')
                
            as_print(func(reg_codes[parts[1]], reg_codes[parts[2]]))
            
        elif inst_type == 'R8U':
            if len(parts) != 3:
                sys.exit(f'Error: RR type inst {parts[0]} expects two arguments, found {len(parts)-1}')
            inst, imm, r2 = parts
            if imm[0] != '$':
                # TODO
                sys.exit(f'Error: symbol table not implemented: bad imm {imm} on line {i}')
            parsed_imm = int(imm[1:])
            
            if parsed_imm > 0xFFFF or parsed_imm < 0:
                sys.exit(f'Error: found out of range imm {parsed_imm} for unsigned immediate on line {i}')
                
            if r2 not in reg_codes:
                sys.exit(f'Error: Found invalid register {r2} on line {i}')
                
            as_print(func(parsed_imm, reg_codes[r2]))
            
        elif inst_type == 'R8S':
            pass
        
    
    
    
def main() -> None:
    parser = argparse.ArgumentParser(description='This is the CR16 Assembler V2')
    parser.add_argument('file', nargs='?', help='The asm file to assemble')
    parser.add_argument('-i', '--input', action='store_true', help='Read asm from stdin instead of a file (Reads lines until double new line)')
    args = parser.parse_args()
    
    asm_input = read_stdin() if args.input else open(args.file).readlines()
    
    
    assemble(asm_input)
    

if __name__ == '__main__': main()