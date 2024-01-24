import fileinput

class ALU:
    def __init__(self):
        self.data=bin(0)[2:].rjust(24,'0')
    def modify(self,data):
        self.data=data
    
    #design here all the functions add sub modify
    
    
    def store(self):
        global Ac
        self.data=Ac
        Mbr.buff_modify(self.data)#now mbr is modified with value stored in ac
    def load(self):
        global Ac
        Ac=self.data
    def compare_1(self):
        global Ac
        if(int(self.data,2)>int(Ac,2)):
            Ac=bin(1)[2:].rjust(24,'0')
            return
        Ac=bin(0)[2:].rjust(24,'0')
    def Load_mq_m(self):
        global Mq
        Mq=self.data
    def Load_mq(self):
        global Ac
        global Mq
        Ac=Mq# what to write after $ sign
    def Add(self):
        global Ac
        Ac=bin(int(Ac,2)+int(self.data,2))[2:].rjust(24,'0')
    def Sub(self):
        global Ac
        Ac=bin(int(Ac,2)-int(self.data,2))[2:].rjust(24,'0')
    def Mul(self):
        global Ac
        global Mq
        temp=bin(int(Ac,2)*int(self.data,2))[2:].rjust(48,'0')
        Mq=temp[:24]
        Ac=temp[25:]
    def Div(self):
        global Ac
        global Mq
        Mq=bin(int(self.data,2)%int(Ac,2))[2:].rjust(24,'0')
        Ac=bin(int(self.data,2)//int(Ac,2))[2:].rjust(24,'0')
    def And(self):
        global Ac
        if(int(self.data,2)>=1):
            if(int(Ac,2)>=1):
                Ac=bin(1)[2:].rjust(24,'0')
                return
        Ac=bin(0)[2:].rjust(24,'0')
    
    def Or(self):
        global Ac
        if(int(self.data,2)==0):
            if(int(Ac,2)==0):
                return # no need to change the value of ac as is alreay zero
        Ac=bin(1)[2:].rjust(24,'0')
    
    def Not(self):
        global Ac
        if(int(Ac,2)==0):
            Ac=bin(1)[2:].rjust(24,'0')
            return
        Ac=bin(0)[2:].rjust(24,'0')

    def jumpR1(self):
        global Ac
        if(int(Ac,2)==1):
            Mbr.buff_modify(bin(1)[2:].rjust(24,'0'))
            return
        Mbr.buff_modify(bin(0)[2:].rjust(24,'0'))
    def jumpL1(self):
        global Ac
        if(int(Ac,2)==1):
            Mbr.buff_modify(bin(1)[2:].rjust(24,'0'))
            return
        Mbr.buff_modify(bin(0)[2:].rjust(24,'0'))
    def do_nothing(self):
        Mbr.buff_modify(bin(1)[2:].rjust(24,'0'))
    def compare_2(self):
        global Ac
        if(int(self.data,2)<int(Ac,2)):
            Ac=bin(1)[2:].rjust(24,'0')
            return
        Ac=bin(0)[2:].rjust(24,'0')
    
Alu=ALU()

class IBR:
    def __init__(self):
        self.reg=bin(0)[2:].rjust(7,'0')
        self.flag=bin(1)[2:].rjust(5,'0')
    def modify(self,instruction):
        
        self.reg=instruction[5:12]
        self.flag=instruction[0:5] # 00000 in ibr.flag is deactivated state of Ibr
    
    def deactivate(self):
        self.flag=bin(0)[2:].rjust(5,'0')
    
    def distribute(self):
        global Mar,Ir
        if(self.flag!=bin(0)[2:].rjust(5,'0')):
            Mar=self.reg
            Ir=self.flag
        else:
            Ir=self.flag
class MBR:
    def __init__(self):
        self.reg=bin(0)[2:].rjust(24,'0')
        self.flag=bin(0)[2:].rjust(5,'0')
        self.buff=bin(0)[2:].rjust(24,'0')
        self.Operations={
'10101':Alu.load,'00001':Alu.store,'00100':Alu.compare_1,
'00101':Alu.Load_mq_m,'00110':Alu.Load_mq,'00111':Alu.jumpL1,
'01000':Alu.jumpR1,'01011':Alu.Add,'01100':Alu.Sub,
'01101':Alu.Mul,'01110':Alu.Div,'01111':Alu.do_nothing,
'10000':Alu.And,'10001':Alu.Or,'10010':Alu.Not,
'10011':Alu.do_nothing,'10100':Alu.do_nothing,'11010':Alu.compare_2
}
    def reg_modify(self,val):
        self.reg=val
    
    def flag_modify(self,flag):
        self.flag=flag

    def buff_modify(self,new_value):
        self.buff=new_value    

    def do_task(self):
        Alu.modify(self.reg)# when the opcode corresponds to jump statement #gives the value stored in Mar to Pc and no alu operations are performed
        global Pc,Mar
        self.Operations[self.flag]()
        
        if(self.flag=='00001'):
            memory.insert(Mar,self.buff)
            self.buff=(bin(0)[2:].rjust(24,'0'))
            
        elif(self.buff==bin(1)[2:].rjust(24,'0')):
            Pc=Mar
            Ibr.deactivate()
            self.buff=(bin(0)[2:].rjust(24,'0'))
        
    def split_instruction(self):
        global Mar,Ir
        Ibr.modify(self.reg[12:24])
        Mar=self.reg[5:12]
        Ir=self.reg[0:5]
    
    
class Memory:
    #4 types of spaces in memory Program Instructions storage ,Program data storage,Buffer,
    def __init__(self):
        self.memory=['' for i in range(128)]
        self.count=0
    
    def value(self):
        global Mar
        return self.memory[int(Mar,2)]
    
    def insert(self,pos,val):
        self.memory[int(pos,2)]=val
    
    def load_ins(self,val):
        self.memory[(self.count//2)+65]+=val
        self.count+=1

def Fetch():
    print("In fetch stage")
    global Mar
    global Pc
    Mar=Pc
    print("Address goes from Pc-> Mar")
    Mbr.reg_modify(memory.value())
    print("Mar gives memory the address and the corresponding value is trasfered to MBR")
    Mbr.split_instruction()
    print("The instruction is now being split into IBR and IR and MAR")
    #Fetch cycle is completed

def Decode():
    print("In Decode stage")
    Mbr.flag_modify(Ir)
    print("now Ir gives control signal to MBR")
    Mbr.reg_modify(memory.value())
    print("The value stored in Memory is transfered to MBR")

def Execute():
    print("In execute stage")
    Mbr.do_task()#now the values are given to alu and alu then perform operations on those values
    Ibr.distribute()#if it was a jump statement then ir is deactivated during process mbr do task

#HOW TO JUMP TO FETCH STAGE AGAIN WHEN PC IS modified BY JUmp Statement
#we solved this by using ir.flag if ir.flag ==0 then do jump

#end changes the value of pc to 64 which signify end of program and instructions are stored in memory from 65 memory address
Pc = bin(64)[2:].rjust(7,'0') # is an pointer to a instruction space in the memory
Ir=bin(0)[2:].rjust(5,'0')
Mar = bin(0)[2:].rjust(7,'0')
Ac=bin(0)[2:].rjust(24,'0')
Mq=bin(0)[2:].rjust(24,'0')
memory=Memory()
Mbr=MBR()
Ibr=IBR()
#Loading instructions into the mmeory

for line in fileinput.input(files="MACHINE_CODE"):
    if(line=='\n'):
        break
    memory.load_ins(line.rstrip())
#start of program
Pc=(bin(1+int(Pc,2))[2:]).rjust(7,'0')
memory.insert(bin(32)[2:].rjust(7,'0'),bin(12345)[2:].rjust(24,'0')) # n stored here
memory.insert(bin(33)[2:].rjust(7,'0'),bin(0)[2:].rjust(24,'0')) # sum stored here
memory.insert(bin(16)[2:].rjust(7,'0'),bin(0)[2:].rjust(24,'0'))
memory.insert(bin(17)[2:].rjust(7,'0'),bin(10)[2:].rjust(24,'0'))
while(Pc!=(bin(64)[2:]).rjust(7,'0')):
    Fetch()
    Decode()
    Execute()
    if(Ir==bin(0)[2:].rjust(5,'0')):#we can also do Ibr.flag==0 here
        continue
    Decode()
    Execute()
    if(Ir==bin(0)[2:].rjust(5,'0')):#we can also do Ibr.flag==0 here
        continue
    Pc=(bin(1+int(Pc,2))[2:]).rjust(7,'0')
#end of program
print(f"the value stored inside the Accumulator is {int(Ac,2)} ")



# Write any errors you get here

