#
# Translator RISC-V RV32I
# Assembler to machine code
# Author: Aleksandra Gontsova
# 2024
#

import argparse
import sys

parser = argparse.ArgumentParser(description="Translate assembler RISC-V (ISA RV32I) to machine code. \n The program must be written in small letters, pseudoinstructions are not processed, labels must be on a separate line")
parser.add_argument("-f", default=None, help = "Input assembler file")
parser.add_argument("-m", default="1", help = "Make output binary file for ModelSim (with _ ), default 1, set 0 to off")
parser.add_argument("-bin", default=None, help = "Make output binary file, set 1 to on")
parser.add_argument("-hex", default=None, help = "Make output hex file, set 1 to on")
args = parser.parse_args()

flag_m = args.m
flag_b = args.bin
flag_h = args.hex
filename = args.f

if filename == None:
    print ("No input file. Nothing to do. Enter -h for more info. Exit")
    sys.exit()

if (flag_m != "1" and flag_b != "1" and flag_h != "1"):
    print ("Nothing to do. Enter -h for more info. Exit")
    sys.exit()


# m - int, p - int
def make_immediate( m, p ):
    imm = ""
    if (m < 0):
        m = 2**p + m
    c = int(m % 2)
    d = int(m / 2)
    imm = imm + str(c)
    while (d):
        c = d % 2
        d = int(int(d)/2)
        imm = str(int(c)) + imm
    if (m>=0):
        for j in range(p-len(imm)):
            imm = "0" + imm
    return (imm)

# s - str
def make_hex(s):
    i=3
    h=0
    s_hex=""
    for j in range (len(s)):
        h = h + int (s[j]) * (2**i)
        i = i - 1
        if i == -1:
            i = 3
            s_hex = s_hex + dict_hex[h]
            h = 0
    return s_hex

OP =          "0110011"
OP_IMM =      "0010011"
LUI =         "0110111"
AUIPC =       "0010111"
BRANCH =      "1100011"
LOAD =        "0000011"
STORE =       "0100011"
JAL =         "1101111"
JALR =        "1100111"

#subs_opcode = {}

subs_reg = {"zero": "00000", "x0": "00000", "ra": "00001", "x1": "00001", "sp": "00010", "x2": "00010", "gp": "00011", "x3": "00011", "tp": "00100", "x4": "00100", "x5": "00101", "t0": "00101", "x6": "00110", "t1": "00110", "x7":"00111", "t2": "00111", "x8": "01000", "s0": "01000", "fp": "01000", "x9": "01001", "s1": "01001", "x10": "01010", "a0": "01010", "x11": "01011", "a1":"01011", "x12": "01100","a2": "01100", "x13": "01101","a3":"01101", "x14": "01110", "a4": "01110", "x15": "01111", "a5": "01111", "x16": "10000", "a6": "10000", "x17": "10001", "a7": "10001", "x18": "10010", "s2": "10010", "x19": "10011", "s3": "10011", "x20": "10100", "s4": "10100", "x21": "10101", "s5": "10101", "x22": "10110", "s6": "10110", "x23": "10111", "s7": "10111", "x24": "11000", "s8": "11000", "x25": "11001", "s9": "11001", "x26": "11010", "s10": "11010", "x27": "11011", "s11": "11011", "x28": "11100", "t3": "11100", "x29": "11101", "t4": "11101", "x30": "11110", "t5": "11110", "x31": "11111", "t6": "11111"}

subs_op = {"add": "000", "sub": "000","sll": "001", "slt": "010", "sltu":"011", "xor":"100", "srl":"101", "sra":"101", "or":"110", "and":"111"}
subs_opimm = {"addi": "000", "slli": "001", "slti": "010", "sltui":"011", "xori":"100", "srli":"101", "srai":"101", "ori":"110", "andi": "111", "jalr":"000"}
subs_branch = {"beq": "000", "bne":"001", "blt":"100", "bge":"101", "bltu":"110", "bgeu":"111"}
subs_load = {"lw":"010", "lh":"001", "lb":"000", "lhu":"101", "lbu":"100"}
subs_store = {"sw":"010","sh":"001", "sb":"000"}
subs_u = {"lui":"0", "auipc":"0"}
subs_j = {"jal":"0"}

dict_hex = {0:"0", 1:"1", 2:"2", 3:"3", 4:"4", 5:"5", 6:"6", 7:"7", 8:"8", 9:"9", 10:"a", 11:"b", 12:"c", 13:"d", 14:"e", 15:"f"}

dict_m={}
i_comm=0
i_str=0
arg1 = ""
arg2 = ""
imm = ""
immm=""
immb=""
immh=""
f=0
opcode=""

file = open (filename, "r")

if flag_m=="1":
    outfile = open ("outm.txt","w")
if flag_b=="1":
    outfileb = open ("outb.txt","w")
if flag_h=="1":
    outfileh = open ("outh.txt","w")
lines = file.readlines()

#проходимся по программе и ищем все метки
for line in lines:
    f=0
    if line[0] == "#":
        x=0
    elif line[0] != "\n":
        try:
            ind = line.index(' ')
            comm = line[0:ind]
            if subs_op.get(comm) != None:
                f=1
            elif subs_opimm.get (comm) != None:
                f=2
            elif subs_branch.get(comm) != None:
                f=3
            elif subs_load.get(comm) != None:
                f=4
            elif subs_store.get(comm) != None:
                f=5
            elif subs_u.get(comm) != None:
                f=6
            elif subs_j.get(comm) != None:
                f=7
            else:
                f=0
        except ValueError:
            x=0
        try:
            ind = line.index(':') 
            dict_m[line[0:ind]] = i_comm*4 #
        except ValueError:
            x=0
    if f!=0:
        i_comm = i_comm + 1
    i_str = i_str + 1

#print (dict_m)
i_comm=0
i_str=0

file = open (filename, "r")
lines = file.readlines()

# второй проход по файлу для парсинга команд
for line in lines:
    immm = ""
    imm = ""
    f=0
    print ("line #" + str(i_str) + "(" + str(i_comm) + "):  ", line)
    if line[0] == "#":
        x=0
    elif line[0] != "\n":
        try:
            ind = line.index(':')
            x = 1
        except ValueError:
            x = 0
        try:
            ind = line.index(' ')
            comm = line[0:ind]
            if subs_op.get(comm) != None:
                f=1
            elif subs_opimm.get (comm) != None:
                f=2
            elif subs_branch.get(comm) != None:
                f=3
            elif subs_load.get(comm) != None:
                f=4
            elif subs_store.get(comm) != None:
                f=5
            elif subs_u.get(comm) != None:
                f=6
            elif subs_j.get(comm) != None:
                f=7
            else:
                f=0

            if f==1 or f==2 or f==3:
                ss = line[ind:].strip()
                ind2 = ss.index(',')
                arg1 = ss[:ind2]
                ss = ss [ind2+1:].strip()
                ind3 = ss.index(",")
                arg2 = ss[:ind3]
                ss = ss[ind3+1:].strip()
                try:
                    ind4 = ss.index("#")
                    arg3 = ss[:ind4].strip()
                except ValueError:
                    try:
                        ind4=ss.strip().index(" ")
                        arg3=ss[:ind4].strip()
                        if len (ss[ind4:])!=0:
                            print ("Error (line " + str(i_str) +"): unknown letters")
                    except ValueError:
                        arg3 = ss.strip()
            elif f==4 or f==5:
                ss = line[ind:].strip()
                ind2 = ss.index(',')
                arg1 = ss[:ind2]
                ss = ss [ind2+1:].strip()
                ind3 = ss.index("(")
                arg2 = ss[:ind3].strip()
                ss = ss[ind3+1:].strip()
                ind4 = ss.index(")")
                arg3 = ss[:ind4]
                try:
                    ind4 = ss.index("#")
                except ValueError:
                    try:
                        if len (ss[ind4+1:])!=0:
                            print ("Error (line " + str(i_str) +"): unknown letters")
                    except:
                        x=0
            elif f==6 or f==7:
                ss = line[ind:].strip()
                ind2 = ss.index(',')
                arg1 = ss[:ind2]
                ss = ss [ind2+1:].strip()
                try:
                    ind3 = ss.index("#")
                    arg2 = ss[:ind3].strip()
                except ValueError:
                    try:
                        ind4=ss.strip().index(" ")
                        arg2=ss[:ind4].strip()
                        if len (ss[ind4:])!=0:
                            print ("Error (line " + str(i_str) +"): unknown letters")
                    except ValueError:
                        arg2 = ss.strip()

#------------ R-type -------------------------------------------
            if f==1:
                funct7 = ""
                if comm == "sub" or comm == "sra":
                    funct7 = "0100000"
                else:
                    funct7 = "0000000"
                immm = funct7 + "_" + subs_reg[arg3] + "_" + subs_reg[arg2] + "_" + subs_op[comm] + "_" + subs_reg[arg1] + "_" + OP
                immb = funct7 + subs_reg[arg3] + subs_reg[arg2] + subs_op[comm] + subs_reg[arg1] + OP
                immh = make_hex(immb)
                if flag_m=="1":
                    outfile.writelines(immm)
                    outfile.writelines("\n")
                if flag_b=="1":
                    outfileb.writelines(immb)
                    outfileb.writelines("\n")
                if flag_h=="1":
                    outfileh.writelines(immh)
                    outfileh.writelines("\n")
                
#------------ I-type -------------------------------------------
            elif f==2:
                imm = make_immediate (int(arg3), 12)
                if comm == "jalr":
                    opcode = JALR
                else:
                    opcode = OP_IMM
                if comm == "slli" or comm == "srli":
                    imm = "0000000" + imm[7:12]
                elif comm == "srai":
                    imm = "0100000" + imm[7:12]
                if flag_m:
                    immm = imm + "_" + subs_reg[arg2] + "_" + subs_opimm[comm] + "_" + subs_reg[arg1] + "_" + opcode
                if flag_b or flag_h:
                    immb = imm + subs_reg[arg2] + subs_opimm[comm] + subs_reg[arg1] + opcode
                if flag_h:
                    immh = make_hex(immb)
                if flag_m=="1":
                    outfile.writelines(immm)
                    outfile.writelines("\n")
                if flag_b=="1":
                    outfileb.writelines(immb)
                    outfileb.writelines("\n")
                if flag_h=="1":
                    outfileh.writelines(immh)
                    outfileh.writelines("\n")
#------------ B-type -------------------------------------------
            elif f==3:
                if dict_m.get(arg3)!=None:
                    m = int(dict_m[arg3]) - i_comm*4
                else:
                    print ("Error (line " + str(i_str)+ "): Unknow label")
                    m = 0
                imm = make_immediate (m, 13)
                immm = imm[0] + "_" + imm[2:8] + "_" + subs_reg[arg2] + "_" + subs_reg[arg1] + "_" + subs_branch[comm] + "_" + imm[8:12] + "_" + imm[1] + "_" + BRANCH
                immb = imm[0] + imm[2:8] + subs_reg[arg2] + subs_reg[arg1] + subs_branch[comm] + imm[8:12] + imm[1] + BRANCH
                immh = make_hex(immb)
                if flag_m=="1":
                    outfile.writelines(immm)
                    outfile.writelines("\n")
                if flag_b=="1":
                    outfileb.writelines(immb)
                    outfileb.writelines("\n")
                if flag_h=="1":
                    outfileh.writelines(immh)
                    outfileh.writelines("\n")
#------------ LOAD-type -------------------------------------------
            elif f==4:
                imm = make_immediate (int(arg2), 12)
                immm = imm + "_" + subs_reg[arg3] + "_" + subs_load[comm] + "_" + subs_reg[arg1] + "_" + LOAD
                immb =  imm + subs_reg[arg3] + subs_load[comm] + subs_reg[arg1] + LOAD
                immh = make_hex(immb)
                if flag_m=="1":
                    outfile.writelines(immm)
                    outfile.writelines("\n")
                if flag_b=="1":
                    outfileb.writelines(immb)
                    outfileb.writelines("\n")
                if flag_h=="1":
                    outfileh.writelines(immh)
                    outfileh.writelines("\n")
#------------ STORE-type -------------------------------------------
            elif f==5:
                imm = make_immediate (int(arg2), 12)
                immm = imm[0:7] + "_" + subs_reg[arg1] + "_" + subs_reg[arg3] + "_" + subs_store[comm] + "_" + imm[7:12] + "_" + STORE
                immb = imm[0:7] + subs_reg[arg1] + subs_reg[arg3] + subs_store[comm] + imm[7:12] + STORE
                immh = make_hex(immb)
                if flag_m=="1":
                    outfile.writelines(immm)
                    outfile.writelines("\n")
                if flag_b=="1":
                    outfileb.writelines(immb)
                    outfileb.writelines("\n")
                if flag_h=="1":
                    outfileh.writelines(immh)
                    outfileh.writelines("\n")
#------------ U-type -------------------------------------------
            elif f==6:
                imm = make_immediate (int(arg2), 20)
                if (comm == "lui"):
                    opcode = LUI
                elif(comm == "auipc"):
                    opcode = AUIPC
                else:
                    opcode = ""
                immm = imm + "_" + subs_reg[arg1] + "_" + opcode
                immb = imm + subs_reg[arg1] + opcode
                immh = make_hex(immb)
                if flag_m=="1":
                    outfile.writelines(immm)
                    outfile.writelines("\n")
                if flag_b=="1":
                    outfileb.writelines(immb)
                    outfileb.writelines("\n")
                if flag_h=="1":
                    outfileh.writelines(immh)
                    outfileh.writelines("\n")
#------------ J-type -------------------------------------------
            elif f==7:
                if dict_m.get (arg2)!=None:
                    m = int(dict_m[arg2]) - i_comm*4
                else:
                    print ("Error (line " + str(i_str)+ "): Unknow label")
                    m = 0
                imm = make_immediate (m, 21)
                immm = imm[0] + "_" + imm[10:20] + "_" + imm[9] + "_" + imm[1:9] + "_" + subs_reg[arg1] + "_" + JAL
                immb = imm[0] + imm[10:20] + imm[9] + imm[1:9] + subs_reg[arg1] + JAL
                immh = make_hex(immb)
                if flag_m=="1":
                    outfile.writelines(immm)
                    outfile.writelines("\n")
                if flag_b=="1":
                    outfileb.writelines(immb)
                    outfileb.writelines("\n")
                if flag_h=="1":
                    outfileh.writelines(immh)
                    outfileh.writelines("\n")
            else:
                print ("Error (line " + str (i_str) + ") Unknow command")
        except ValueError:
            if x!=1:
                print ("Error (line " + str (i_str) + ")  Not command!")
            else:
                x=0
    if f!=0:
        i_comm = i_comm + 1
    i_str = i_str + 1



