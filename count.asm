# A loop that sums 0 to 10, 
#  then stores at address 0xFF
MOVI $10 %r1 # r1 is i
MOVI $0 %r2  # r2 is sum
.loop
ADD %r1 %r2
SUBI 1 %r1
CMP %r0 %r1
BNE .loop
MOVI $255 %r3
STOR %r2 %r3