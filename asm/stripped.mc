MOVI $5 %r2 
MOVI $2 %r3 
MOV %r2 %r8 
MOV %r3 %r9 
MOVI .add %rA 
JAL %rA %rA 
LUI $64 %r6 
STOR %r8 %r6 
BUC .end 
MOV %r8 %r1 
ADD %r9 %r1 
JUC %rA 
