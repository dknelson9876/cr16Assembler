import os
import sys
import argparse

labels = {}
jpoint_instrs = {}
macros : dict[str,str] = {}

RAM_START = 0x2000
FILE_LENGTH = 0x4000

r_type_insts =   {'ADD',  'ADDU',  'ADDC',  'MUL',  'SUB',  'SUBC',  'CMP',  'AND',  'OR',  'XOR',  'MOV'}
i_type_insts =   {'ADDI', 'ADDUI', 'ADDCI', 'MULI', 'SUBI', 'SUBCI', 'CMPI', 'ANDI', 'ORI', 'XORI', 'MOVI', 'LUI'}
sh_type_insts =  {'LSH', 'ALSH'}
shi_type_insts = {'LSHI', 'ALSHI'}
b_type_insts =   {'BEQ', 'BNE', 'BGE', 'BCS', 'BCC', 'BHI', 'BLS', 'BLO', 'BHS', 'BGT', 'BLE', 'BFS', 'BFC', 'BLT', 'BUC'}
j_type_insts =   {'JEQ', 'JNE', 'JGE', 'JCS', 'JCC', 'JHI', 'JLS', 'JLO', 'JHS', 'JGT', 'JLE', 'JFS', 'JFC', 'JLT', 'JUC'}
spec_type_insts= {'LOAD', 'STOR', 'JAL'}

sign_ext_imm =   {'ADDI', 'ADDUI', 'ADDCI', 'MULI', 'SUBI', 'SUBCI', 'CMPI'}
zero_ext_imm =   {'ANDI', 'ORI', 'XORI', 'MOVI', 'LUI'}

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
    'rA':  'E',
    'rsp': 'F'
}

inst_codes : dict[str,str] = {
    'REGISTER_TYPE': '0',
    'WAIT':  '0',
    'AND':   '1',
    'ANDI':  '1',
    'OR':    '2',
    'ORI':   '2',
    'XOR':   '3',
    'XORI':  '3',

    'ADD':   '5',
    'ADDI':  '5',
    'ADDU':  '6',
    'ADDUI': '6',
    'ADDC':  '7',
    'ADDCI': '7',
    'MOV':   'D',
    'MOVI':  'D',
    'MUL':   'E',
    'MULI':  'E',
    'SUB':   '9',
    'SUBI':  '9',
    'SUBC':  'A',
    'SUBCI': 'A',
    'CMP':   'B',
    'CMPI':  'B',

    'SHIFT_TYPE': '8',
    'LSH':   '4',
    'LSHI':  '0',
    'ASHU':  '4',
    'ASHUI': '2',

    'LUI':  'F',

    'SPECIAL_TYPE': '4',
    'LOAD': '0',
    'LPR':  '1',
    'SNXB': '2',
    'DI':   '3',
    'STOR': '4',
    'SPR':  '5',
    'ZRXB': '6',
    'EI':   '7',
    'JAL':  '8',
    'RETX': '9',
    'TBIT': 'A',
    'EXCP': 'B',
    'TBITI':'E',

    'BRANCH': 'C',
    'JUMP': 'C',

    'EQ' : '0',
    'NE' : '1',
    'CS' : '2',
    'CC' : '3',
    'HI' : '4',
    'LS' : '5',
    'GT' : '6',
    'LE' : '7',
    'FS' : '8',
    'FC' : '9',
    'LO' : 'A',
    'HS' : 'B',
    'LT' : 'C',
    'GE' : 'D',
    'UC' : 'E'
}

# from https://stackoverflow.com/questions/38834378/path-to-a-directory-as-argparse-argument
def dir_path(path: str) -> str:
    """Check if a str is a valid file path. Returns the path if it's valid, else raises 
        ArgumentTypeError

    Args:
        path (str): The str to check

    Raises:
        argparse.ArgumentTypeError: if path is not a valid file path

    Returns:
        str: path, if it is valid
    """
    if os.path.isdir(path):
        return path
    else:
        raise argparse.ArgumentTypeError(f"readable_dir:{path} is not a valid path")

def replaceLabel(label):
    def r(l):
        if (l[0] == '.'):
            return '$' + str(labels[l])
        else:
            return l

    if (label.startswith('JPT')):
        return label
    else:
        m = map(r, label.split())
        return ' '.join(m)

def replaceMacros(parts: list[str]):
    toreturn: list[str] = []
    if len(parts) > 0 and parts[0] == '`define': return []
    for s in parts:
        if s[0] == '`':
            if s[1:] in macros:
                toreturn.append(macros[s[1:]])
            else:
                sys.exit(f"Undefined macro: {s}")
        else:
            toreturn.append(s)
    return toreturn

    
def assemble(filename: str):
    # find the labels and their addresses
    f = open(filename, 'r')

    address = -1

    # Build the dict for resolving labels
    for x in f:
        line = x.split('#')[0] # discard comment at end of line
        parts = line.split()
        
        if len(parts) > 0:
            if line[0] == '.':
                labelAddress = address + 1

                if labelAddress % 2 == 0:
                    odd = False
                else:
                    odd = True
                    labelAddress -= 1
                    
                count = 0
                # reduce to shift for 8-bit immediate
                while labelAddress > 127:
                    labelAddress /= 2
                    count += 1

                label = parts.pop(0)

                jpoint_instrs[label] = {
                    'initial_immd': labelAddress,
                    'shift_count': count,
                    'is_odd': odd	
                }	
                if odd:
                    # if it is odd, we have to correct for the -1 above
                    labels[label] = labelAddress + 1
                else:
                    labels[label] = labelAddress
            else:
                address = address + 1

    f.seek(0)

    # Find all macro definitions
    for x in f:
        line = x.split('#')[0]
        parts = line.split()

        if len(parts) > 0 and parts[0]=='`define':
            macros[parts[1]] = parts[2]



    f.close()

    print(f"Labels found: {labels}")
    print(f'Macros found: {macros}')

    f = open(filename, 'r')
    filename = filename.replace('\\', '/')
    start = filename.rindex('/')+1 if '/' in filename else 0
    out_name = f"{output_dir}{filename[start:filename.rindex('.')]}.dat"
    wf = open(f"{out_name}", 'w')
    sf = open(f'{output_dir}stripped.mc', 'w')

    ram = False
    address = -1
    for i, x in enumerate(f):
        line = x.split('#')[0] # discard comment at end of line
        parts = replaceMacros(line.split())
        if len(parts) > 0 and line[0] == '@':
            ram = True
            break
        if len(parts) > 0 and line[0] != '.' and line[0] != '`':
            for part in parts:
                sf.write(part + ' ')
            sf.write('\n')
            address = address + 1
            instr = parts.pop(0).upper()
            if instr == 'WAIT':
                wf.write('0000\n')
            elif instr in r_type_insts: # ----------------------------------------------------------------------------------------
                # i.e. ADD %r1 %r2 -> 0251
                if len(parts) != 2:
                    sys.exit(f'ERROR: Wrong number of args on line {i+1} in instruction {x}\n\tExpected: 2, Found: {len(parts)}')
                else:
                    r_src, r_dst = parts
                    if r_src not in reg_codes or r_dst not in reg_codes:
                        sys.exit(f'ERROR: Unrecognized register on line {i+1} in instruction {x}')
                    else:
                        wf.write(inst_codes['REGISTER_TYPE'] + reg_codes[r_dst] + inst_codes[instr] + reg_codes[r_src] + '\n')
            elif instr in i_type_insts: # ----------------------------------------------------------------------------------------
                if len(parts) != 2:
                    sys.exit(f'ERROR: Wrong number of args on line {i+1} in instruction {x}\n\tExpected: 2, Found: {len(parts)}')
                else:
                    imm, r_dst = parts
                    if r_dst not in reg_codes:
                        sys.exit(f'ERROR: Unrecognized register on line {i+1} in instruction {x}')
                    if imm[0] == '$':
                        parsed_imm = int(imm[1:])
                    elif imm[0] == '.':
                        parsed_imm = labels[imm] - address
                    else:
                        sys.exit(f'ERROR: Badly formatted imm on line {i+1} in instruction {x}'
                                +f'\n\tExpected imm to start with: \'$\', but found: \'{imm[0]}\'')

                    if parsed_imm > 0xFF or parsed_imm < -128:
                        sys.exit(f'ERROR: Out of range imm on line {i+1} in instruction {x}'
                                +f'\n\tImmediate must be between -127 and 255, found {parsed_imm}')
                    if instr in sign_ext_imm:
                        if parsed_imm > 127:
                            print(f'WARNING: Found large imm that will be sign extended on line {i+1} in instruction {x}'
                                    +f'\n\t{parsed_imm} will become {int.from_bytes(parsed_imm.to_bytes(1, byteorder="big"), byteorder="big", signed=True)}')
                            # That funkiness in that print is to cast to a byte, then back to an int using 2's C
                    elif instr in zero_ext_imm:
                        if parsed_imm < 0:
                            print(f'WARNING: Found negative imm that will be zero extended on line {i+1} in instruction {x}'
                                    +f'\n\t{parsed_imm} will become {parsed_imm & 0xFF}')
                    else:
                        sys.exit(f'CRASHED: Something went horribly wrong. An inst was in the i_type set, I do not know how the imm is extended')
                    formatted_imm = f'{(parsed_imm & 0xFF):02X}'
                    wf.write(inst_codes[instr] + reg_codes[r_dst] + formatted_imm + '\n')
            elif instr in sh_type_insts: # ----------------------------------------------------------------------------------------
                if len(parts) != 2:
                    sys.exit(f'ERROR: Wrong number of args on line {i+1} in instruction {x}\n\tExpected: 2, Found: {len(parts)}')
                else:
                    r_src, r_dst = parts
                    if r_src not in reg_codes or r_dst not in reg_codes:
                        sys.exit(f'ERROR: Unrecognized register on line {i+1} in instruction {x}')
                    else:
                        wf.write(inst_codes['SHIFT_TYPE'] + reg_codes[r_dst] + inst_codes[instr] + reg_codes[r_src] + '\n')
            elif instr in shi_type_insts: # ----------------------------------------------------------------------------------------
                if len(parts) != 2:
                    sys.exit(f'ERROR: Wrong number of args on line {i+1} in instruction {x}\n\tExpected: 2, Found: {len(parts)}')
                else:
                    imm, r_dst = parts
                    if imm[0] != '$':
                        sys.exit(f'ERROR: Badly formatted imm on line {i+1} in instruction {x}'
                                +f'\n\tExpected imm to start with: \'$\', but found \'{imm[0]}\'')
                    if r_dst not in reg_codes:
                        sys.exit(f'ERROR: Unrecognized register on line {i+1} in instruction {x}')
                    else:
                        parsed_imm = int(imm[1:])
                        if parsed_imm > 15 or 0 > parsed_imm:
                            sys.exit(f'ERROR: Out of range imm on line {i+1} in inst {x}'
                                    +f'\n\tImmediate must be between 0 and 15, found {parsed_imm}')
                        else:  
                            formatted_imm = f'{parsed_imm:01X}'
                            sign_bit = parsed_imm < 0
                            # TODO: Bandaid fix, ASHUI is now unsupported
                            wf.write('8' + reg_codes[r_dst] + str(int(sign_bit)) + formatted_imm + '\n')
            elif instr in b_type_insts: # ----------------------------------------------------------------------------------------
                if len(parts) != 1:
                    sys.exit(f'ERROR: Wrong number of args on line {i+1} in instruction {x}\n\tExpected: 1, Found: {len(parts)}')
                else:
                    displacement = parts[0]
                    if displacement[0] == '$': # if displacement is imm
                        parsed_disp = int(displacement[1:]) # cut off first char
                        if parsed_disp > 255 or -255 > parsed_disp:
                            sys.exit(f'ERROR: Out of range displacement on line {i+1} in inst {x}'
                                    +f'\n\t Displacement must be between -255 and 255, found: {parsed_disp}')
                    elif displacement[0] == '.': # if displacement is label
                        parsed_disp = labels[displacement] - address
                        if parsed_disp > 255 or -255 > parsed_disp:
                            sys.exit(f'ERROR: Out of range displacement on line {i+1} in inst {x}'
                                    +f'\n\t Displacement must be between -255 and 255, but label created displacement: {parsed_disp}')
                    else:
                        sys.exit(f'ERROR: Bad branch displacement on line {i+1} in inst {x}'
                                +f'\n\tCould not recognize {displacement} as a valid imm or label')

                    if parsed_disp >= 0: 
                        formatted_disp = f'{parsed_disp:02X}'
                    else:
                        twos_comp_disp = ((-1 * parsed_disp) ^ 255) + 1
                        formatted_disp = f'{twos_comp_disp:02X}'
                    wf.write(inst_codes['BRANCH'] + inst_codes[instr[1:]] + formatted_disp + '\n')
            elif instr in j_type_insts: # ----------------------------------------------------------------------------------------
                if len(parts) != 1:
                    sys.exit(f'ERROR: Wrong number of args on line {i+1} in instruction {x}\n\tExpected: 1, Found: {len(parts)}')
                else:
                    r_src = parts[0]
                    if r_src not in reg_codes:
                        sys.exit(f'ERROR: Unrecognized register on line {i+1} in instruction {x}')
                    else:
                        wf.write(inst_codes['SPECIAL_TYPE'] + inst_codes[instr[1:]] + inst_codes['JUMP'] + reg_codes[r_src] + '\n')
            elif instr in spec_type_insts:
                if len(parts) != 2:
                    sys.exit(f'ERROR: Wrong number of args on line {i+1} in instruction {x}\n\tExpected: 2, Found: {len(parts)}')
                r_first, r_sec = parts
                if r_first not in reg_codes or r_sec not in reg_codes:
                    sys.exit(f'ERROR: Unrecognized register on line {i+1} in instruction {x}')
                else:
                    wf.write(inst_codes['SPECIAL_TYPE'] + reg_codes[r_first] + inst_codes[instr] + reg_codes[r_sec] + '\n')
            elif instr == 'NOP':
                # Hardcode NOP as OR %r0 %r0
                wf.write('0020\n')

            else: # ----------------------------------------------------------------------------------------
                sys.exit('Syntax Error: not a valid instruction: ' + line)

    if ram:
        while address < RAM_START-1:
            wf.write('0000\n')
            address += 1
        mode = f.readline()
        if mode == 'DECIMAL\n':
            for x in f:
                line = x.split('#')[0] # Remove end of line comments
                if len(line) > 1:
                    parsed_line = int(line[:-1])
                    formatted_line = f'{parsed_line:04X}'
                    wf.write(f'{formatted_line}\n')
                    address += 1
        else:
            sys.exit(f"Unsupported RAM encoding mode: {mode[:-1]}")

    if not short_file:
        while address < FILE_LENGTH-1:
            wf.write('0000\n')
            address = address + 1
    wf.close()
    f.close()

def main():
    # Builds the argument menu and provide the strings used when
    #   `py assembler.py -h` or `py assembler.py --help` is run
    parser = argparse.ArgumentParser(description='This is the CR16 Assembler')
    parser.add_argument('file', nargs='?', help='The asm file to assemble')
    parser.add_argument('--dir', type=dir_path, help='A directory of asm files to assemble')
    parser.add_argument('--dest', type=dir_path, help='A directory to store resulting .dat files')
    parser.add_argument('-s', '--short', action='store_true', help='Do not write 0\'s to size of RAM')
    args = parser.parse_args()

    # Retrieve the information that was provided as flags through the `args` object
    global short_file # should the resulting file be 0 filled to the length of the file?
    short_file: bool = args.short

    global output_dir # where should the resulting file be put
    if args.dest == None:
        if args.dir == None:
            # provided no destination directory or directory to load from
            # Use current folder as output
            output_dir = './'
        else:
            # provided a directory to read from, but no output directory
            # Use provided loading directory as output directory
            output_dir = f'{args.dir}/'
    else:
        # Provided an output directory
        # Use it
        output_dir = f'{args.dest}/'

    if args.file != None:
        # if a single file was provided, assemble it directly
        assemble(args.file)
    elif args.dir != None:
        # if a directory was provided, assemble each file in it
        for f in os.listdir(args.dir):
            assemble(f'{args.dir}/{f}')
    else:
        # if there wasn't a file or directory to load, error out
        sys.exit('argument error: must provide file or directory of files to assemble')
  
if __name__ == "__main__":
    main()
