reg_codes = {
    "R1": 1,
    "R2": 2,
    "R3": 3
}


opcodes: dict = {
    'ADD': ('RR', lambda rsrc, rdst: f'0{rdst:1X}5{rsrc:1X}'),
    'ADDI': ('R8I', lambda imm, rdst: f'5{rdst:1X}{imm:02X}')
}

def main():
    parts = ["ADD", "R1", "R2"]

    if parts[0] not in opcodes:
        print("Error: missing instruction")
        exit(1)

    inst_type, func = opcodes[parts[0]]

    if inst_type == "RR":
        if len(parts) != 3 or parts[1] not in reg_codes or parts[2] not in reg_codes:
            print("Error: bad registers")
            exit(1)
        result = func(reg_codes[parts[1]], reg_codes[parts[2]])
        print(result)
    else:
        print("Error: unsupported instruction type")
        exit(1)


if __name__ == '__main__':
    main()