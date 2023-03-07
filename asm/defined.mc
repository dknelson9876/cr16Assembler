# ---------------------------
# test_jal.asm
# ---------------------------
# Tests the JAL instruction
# ---------------------------
# Loads r2=5, r3=2, then calls the .add subroutine

.start
MOVI $5 %r2 # r2 = 5
MOVI $2 %r3 # r3 = 2
#MOVI .add %r9 # r9 = .add
#JAL %rA %r9 # r1 = .add(5, 2); (store in rA, jump to r9)
MOV %r2 %r8
MOV %r3 %r9
MOVI .add %rA
JAL %rA %rA
# MOV %r2 %r8
# MOV %r3 %r9
# MOVI .add %rA
# JAL %rA %rA
LUI $64 %r6 # r6 = 0x4000
STOR %r8 %r6 # ram[0x4000] = 7
BUC .end # END program

# ADD function
# r1 = r2 + r3
# with rA as return
.add
MOV %r8 %r1
ADD %r9 %r1
JUC %rA


.end
