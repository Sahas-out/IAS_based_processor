import fileinput

class ALU:
    def __init__(self):
        self.data=bin(0)[2:].rjust(24,'0')
    def modify(self,data):
        self.data=data
    
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
        Ac=Mq
    
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
            Mbr.buff_modify(bin(2)[2:].rjust(24,'0'))
            return
        Mbr.buff_modify(bin(0)[2:].rjust(24,'0'))
    
    def jumpL1(self):
        global Ac
        if(int(Ac,2)==1):
            Mbr.buff_modify(bin(1)[2:].rjust(24,'0'))
            return
        Mbr.buff_modify(bin(0)[2:].rjust(24,'0'))
    
    def jumpL(self):
        Mbr.buff_modify(bin(1)[2:].rjust(24,'0'))
    
    def jumpR(self):
        Mbr.buff_modify(bin(2)[2:].rjust(24,'0'))
    
    def end(self):
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
        self.flag=bin(0)[2:].rjust(5,'0')
        self.state=bin(0)[2:].rjust(2,'0')
    def modify(self,instruction):
        self.reg=instruction[5:12]
        self.flag=instruction[0:5] # 00000 in ibr.flag is deactivated state of Ibr
    
    def deactivate(self,state):
        self.state=bin(state)[2:].rjust(2,'0')
    
    def activate(self):
        self.state=bin(0)[2:].rjust(2,'0')
    
    def distribute(self):
        global Mar,Ir
        if(self.state==bin(0)[2:].rjust(2,'0')):
            Mar=self.reg
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
'01101':Alu.Mul,'01110':Alu.Div,'01111':Alu.end,
'10000':Alu.And,'10001':Alu.Or,'10010':Alu.Not,
'10011':Alu.jumpR,'10100':Alu.jumpL,'11010':Alu.compare_2
}
    def reg_modify(self,val):
        self.reg=val
    
    def flag_modify(self,flag):
        self.flag=flag

    def buff_modify(self,new_value):
        self.buff=new_value    

    def instruct_ALU(self):
        Alu.modify(self.reg)# when the opcode corresponds to jump statement #gives the value stored in Mar to Pc and no alu operations are performed
        if(Ibr.state=='10'):
            self.buff=bin(0)[2:].rjust(24,'0')
            self.flag=bin(0)[2:].rjust(5,'0')
            return    
        self.Operations[self.flag]()
    
    def analyze(self):
        global Mar,Pc
        if(self.flag=='00001'):
            memory.insert(Mar,self.buff)
            self.buff=(bin(0)[2:].rjust(24,'0'))
            
        elif(self.buff!=bin(0)[2:].rjust(24,'0')):
            Pc=Mar
            Ibr.deactivate(int(self.buff,2))
            self.buff=(bin(0)[2:].rjust(24,'0'))
        
    def split_instruction(self):
        global Mar,Ir
        Ibr.modify(self.reg[12:24])
        Mar=self.reg[5:12]
        Ir=self.reg[0:5]
    
    
class Memory:
    
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
    global Mar
    global Pc
    Mar=Pc
    Mbr.reg_modify(memory.value())
    Mbr.split_instruction()

def Decode():
    Mbr.flag_modify(Ir)
    Mbr.reg_modify(memory.value())


def Execute():
    Mbr.instruct_ALU()
    Ibr.activate()
    Mbr.analyze()
    Ibr.distribute()
    #if it was a jump statement then ir is deactivated during process mbr do task

# Intailizing registers here
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

# memory.insert(bin(32)[2:].rjust(7,'0'),bin(69069)[2:].rjust(24,'0')) # n stored here
# memory.insert(bin(33)[2:].rjust(7,'0'),bin(0)[2:].rjust(24,'0')) # sum stored here
# memory.insert(bin(16)[2:].rjust(7,'0'),bin(0)[2:].rjust(24,'0')) # temporary value 0 stored in buffer
# memory.insert(bin(17)[2:].rjust(7,'0'),bin(10)[2:].rjust(24,'0')) # temporary value 10 stored in buffer

memory.insert(bin(16)[2:].rjust(7,'0'),bin(1)[2:].rjust(24,'0'))
memory.insert(bin(32)[2:].rjust(7,'0'),bin(8)[2:].rjust(24,'0'))
memory.insert(bin(33)[2:].rjust(7,'0'),bin(1)[2:].rjust(24,'0'))

#start of program
Pc=(bin(1+int(Pc,2))[2:]).rjust(7,'0')
while(Pc!=(bin(64)[2:]).rjust(7,'0')):
    # state 0 : correspond to normal stage
     # state 1 : correspond to jump_l 
    # state 2 : correspond to jump_r
    Fetch()
    Decode()
    Execute()
    if(Ibr.state!=bin(0)[2:].rjust(2,'0')):
        continue
    Decode()
    Execute()
    if(Ibr.state!=bin(0)[2:].rjust(2,'0')):
        continue
    print(f"After step: {int(Pc,2)} value of n is {(int(memory.memory[32],2))} value of sum is {int(memory.memory[33],2)}")
    Pc=(bin(1+int(Pc,2))[2:]).rjust(7,'0')

# End of PRogram
print(f"the value stored inside the Accumulator is {int(Ac,2)} ")



# Write any errors you get here

