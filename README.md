# CR16 Assembler

## Usage

### 1. Consult all '`FILL ME IN`' comments

This includes `RAM_START`, `FILE_LENGTH`, `INST_SETS`, `reg_codes`, `inst_codes`

## CR16 Syntax

These are all pulled from/based on the full [CR16 Programmer's Reference Manual](https://my.eng.utah.edu/~cs3710/handouts/cr16a-prog-ref.pdf), with some syntax additions to help reduce mistakes

- Instruction names are lowercased, but the assembler accepts uppercase
    > `add r0, r3`
- Registers are prefixed by `R` or `r` and are labeled `r0`-`r13`, `rA`, `rSP`
    > `r0`, `r1`, ...
- Labels are prefixed with a `.` (period), and must be the only thing on that line
- Indentation is ignored by the assembler
- Immediate values are prefixed with a `$`, and can be in decimal or hexadecimal
    > `$10`, `$127`, `$0x20`, `$0x100`

# CR16 Assembler

## Register Uses
| reg | use |
|-|-|
| %r0 | reserved hardware 0 |
| %r1 | callee preserved |
| %r2 | callee preserved |
| %r3 | callee preserved |
| %r4 | callee preserved |
| %r5 | callee preserved |
| %r6 | caller preserved |
| %r7 | caller preserved |
| %r8 | parameter/caller preserved |
| %r9 | parameter/caller preserved |
| %rA | return address |
| %rB | return value/parameter/caller preserved |
| %rC | parameter/caller preserved |
| %rD | parameter/caller preserved |
| %gsp(rE) | GPU stack pointer |
| %csp(rF) | CPU stack pointer |

## Calling Conventions

## Copying MIPS syntax