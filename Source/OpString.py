#####   OPERACIONES CON STRINGS

def isEmptyLine(linea):
    if linea.isspace():
        return True
    return False

def removeSpace(linea):
    s=linea
    s=s.strip()
    s=s.strip('\t')
    s=s.strip('\n')
    return s

def stringToIntB(s,b):
    intstr=0
    try:
        intstr=int(s,b)
        return intstr
    except:
        return None

def isOperValid(oper):
    hexoper=stringToIntB(oper,16)
    #print(hexoper)
    if hexoper == None:
        return False
    return True

def operNumber(oper):
    #print('operNumber')
    #print(oper)
    if '$' in oper:
        n=oper.index('$')
        return oper[n+1:]
    try:
        s=hex(int(oper,10))
        return s[2:]
    except:
        return None
    

def numberInBeg(linea):
    if linea[0].isdigit():
        return True
    return False


def getDataFromLine(linea,sep):
    s=removeSpace(linea)
    s=s.replace(' ','')
    s=s.replace('\t','')
    L=s.split(sep)
    #print(L)
    return L

def getDataFromLineNem(linea):
    Data=[]
    sep='+'
    linea=removeSpace(linea)
    linea=linea.replace(' ',sep)
    linea=linea.replace('\t',sep)
    Data=linea.split(sep)
    n=len(Data)
    try:
        for i in range(n):
            Data.remove('')
    except ValueError:
        pass
    return Data
    #k=0
    #for i in lines_space:
    #    del self.lines[i-k]
    #    k=k+1
 


