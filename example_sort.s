#сортировка подсчётом

addi t3, zero, 5
addi t4, zero, 2
addi t5, zero, 4
addi t6, zero, 3

sw t3, 0 (zero)
sw t4, 4 (zero)
sw t5, 8 (zero)
sw t6, 12 (zero)

addi t0, zero, 0 # cnt i
addi t1, zero, 0 # cnt j
addi a2, zero, 0
addi a3, zero, 16
addi a4, zero, 1
addi a5, zero, 24

jal zero, m2

m1:
#записали подсчитанное значение
sw a4, 16 (t1)
jal zero, m3

m2:
#выгрузили цифру
addi t1, zero, 0
addi a2, zero, 0
lw t2, 0 (t0)

m33:
beq t2, a2, m1
addi t1, t1, 4
addi a2, a2, 1
jal zero, m33

m3:
addi t0, t0, 4
beq t0, a3, m4
jal zero, m2

m5:
sw a2, 0 (t1)
addi t1, t1, 4
jal zero, m6

m4:
#изменение значений на новые (в новом порядке)
addi t0, zero, 0
addi t1, zero, 0
addi a2, zero, 0
m44:
lw t2, 16 (t0)
beq t2, a4, m5

m6:
addi t0, t0, 4
addi a2, a2, 1
beq t0, a5, m7
jal zero, m44

m7:
addi zero, zero, 0
