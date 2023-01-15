# ---------------------------
# test_jal.asm
# ---------------------------
# Tests the JAL instruction
# ---------------------------
# Loads r2=5, r3=2, then calls the .add subroutine

.start
MOVI $5 %r2     # r2 = 5
MOVI $2 %r3     # r3 = 2
CALL .add (%r2,%r3)
#   MOV %r2 %r8
#   MOV %r3 %r9
#   MOVI .add %rA
#   JAL %rA %rA
LUI $64 %r6     # r6 = 0x4000
STOR %rB %r6    # ram[0x4000] = 7
BUC .end        # END program

# ADD function
# r8 = r8 + r9
# with rA as return 
.add
    MOV %r8 %rB
    ADD %r9 %rB
    JUC %rA

.end