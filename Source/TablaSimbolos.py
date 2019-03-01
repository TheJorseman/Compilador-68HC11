import pandas as pd
from tkinter import messagebox

def leer_archivo_excel(nombre_archivo):
    print(nombre_archivo)
    set_inst=object()
    try:
        set_inst=pd.ExcelFile(nombre_archivo)
    except Exception as e:
        print('ERROR')
        print(e)
        messagebox.showerror('ERROR','ERROR AL ABRIR EL ARCHIVO DE NEMONICOS')
        return None
    return set_inst

def is_hex(s):
    try:
        int(s, 16)
        return True
    except ValueError:
        return False

class Tabla_Simbolos:
    #Atributos
    Mnemonicos=list()
    DirModes=dict()
    Table_Simbol_Instance=object()
    Instruction_Data=object()
    DirNames=list()
    #Palabras clave
    mnemonico='MNEMONICO'
    opcode='OPCODE'
    byte='Byte'
    #Constructor
    def __init__(self,archivo):
        #Lee Archivo Excel
        self.Instruction_Data=leer_archivo_excel(archivo)
        #Recupera los nombres de los modos de direccionamiento
        self.DirNames=self.Instruction_Data.sheet_names
        self.Mnemonicos=self.Instruction_Data.parse(self.DirNames[0],header=1)[self.mnemonico].values
        #print(self.Mnemonicos)
        self.__getData()
        return
    def __getData(self):
        for moddir in self.DirNames:
            opcodes=self.Instruction_Data.parse(moddir,header=1)['OPCODE'].values
            num_bytes=self.Instruction_Data.parse(moddir,header=1)['Byte'].values   
            if( len(opcodes)==len(self.Mnemonicos) and len(num_bytes)==len(self.Mnemonicos) ):
                opcodes=self.fixOPCodeList(opcodes)
                num_bytes=self.fixOPCodeList(num_bytes)
                self.DirModes[moddir]=(opcodes,num_bytes)
            else:
                print('Algo Anda Mal...')
        #print(self.DirModes)
        return
    def fixOPCodeList(self,lista):
        List=[]
        for i in lista:
            List.append(str(i).replace(' ',''))
        return List
    
    def getOPCode(self,dirmode):
        
        return

