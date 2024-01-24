import fileinput

map_opcode={
'LOAD':'10101','STORE':'00001','COMPARE_1':'00100',
'LOAD_MQ_M':'00101','LOAD_MQ':'00110','JUMP_L+1':'00111',
'JUMP_R+1':'01000','ADD':'01011','SUB':'01100',
'MUL':'01101','DIV':'01110','END':'01111',
'AND':'10000','OR':'10001','NOT':'10010',
'JUMP_R':'10011','JUMP_L':'10100','COMPARE_2':'11010'
}


file1=open('MACHINE_CODE','w')
for line in fileinput.input(files="Asm_langx.txt"):
    if(line=='\n'):
        break
    opcode,address=(line.split(';')[0]).split("$")
    
    if(address==''):
        address='0'
    file1.write(map_opcode[opcode]+f'{int(address):07b}'+'\n')




    