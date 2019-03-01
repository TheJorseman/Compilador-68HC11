########## ETIQUETAS Y VARIABLES
from OpString import *
VarNem='EQU'
def isLab(linea):
    if linea[0].isalpha() and not VarNem in linea.upper():
        return True
    return False

def isVar(linea):
    if VarNem in linea.upper():
        return True
    return False


def nameIsValid(name):
    if numberInBeg(name):
        return False
    return True

    
