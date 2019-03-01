from OpString import *

#####   FUNCIONES PARA VALIDAR COMENTARIOS ###########
##CONSTANTES
SimbolComment='*'
SimbolsMnem=[' ','\t','\n']
#CHECK COMMENT **************************************************
def is_Comment(line):
    s=removeSpace(line)
    if s[0]==SimbolComment:
        return True
    return False
def containsComm(linea):
    if SimbolComment in linea:
        return True
    return False

def getStringComm(line):
    n_com=line.index(SimbolComment)
    comm=line[n_com:]
    data=line[:n_com]
    #print(data)
    #print(comm)
    return data,comm
 

    
