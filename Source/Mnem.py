from OpString import *
import math
###### Funciones Mnemonicos ########
Inicio='ORG'
Fin='END'

def isInicio(linea):
    if Inicio in linea:
        return True
    return False

def check_Inicio(Data):
    #print(Data)
    if len(Data)==2:
        if Data[0].upper()==Inicio:
            if not self.containsBegin:
                inicio=self.simpleOper(Data[1])
                self.ORG=inicio
                self.InM=int(self.ORG,16)
                self.containsBegin=True
            return True
    return False

def isEnd(linea):
    if Fin in linea:
        return True
    return False

def AdjustOper(op,OpCode,n_bytes):
    m=math.ceil(len(OpCode)/2)
    op=op.rjust((n_bytes-m)*2,'0')
    return op

def compA2(n):
    m=abs(n)
    A2=bin((m^0xffff)+1)[2:]
    Oper=hex(int(A2,2))[2:].upper()
    return Oper
