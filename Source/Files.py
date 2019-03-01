#####   FUNCIONES PARA VALIDAR COMENTARIOS ###########
from tkinter import messagebox
##CONSTANTES
modeFile='r'

def ListFromFile(nombre):
    File=object()
    Lista_f=list()
    try:
        File=open(nombre,modeFile)
    except:
        print('Error al leer el archivo '+nombre)
        messagebox.showerror('ERROR','ERROR AL ABRIR EL ARCHIVO'+'nonbre')
        return None
    for linea in File:
        #print(linea)
        linea=linea.strip()
        linea=linea.strip('\n')
        linea=linea.strip('\t')
        Lista_f.append(linea)
    return Lista_f
def getName(path):
    k=path.rindex('/')
    return path[k+1:]
def getPath(path):
    k=path.rindex('/')
    return path[:k+1]
