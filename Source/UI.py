from tkinter import *
import tkinter.ttk
from tkinter import messagebox
from tkinter import filedialog


import pandas as pd
#Clases Propias
from TablaSimbolos import *
from Scanner import *


#ARCHIVOS DEL PROGRAMA
nombre_xls='MC68HC11.xlsx'
error_list='Errores.txt'
saltos='MnemLab.txt'
html='BaseHTML.txt'
Table=Tabla_Simbolos(nombre_xls)


class Ventana:
    #Ventana
    ventana=object()
    root=object()
    #Parámetros
    tx=int()
    ty=int()
    Menu=object()
    FileMenu=object()
    #EditMenu=object()
    ConfigMenu=object()
    Help=object()

    FilePath=''

    TextHolder=object()
    ErrorHolder=object()
    #LABELS
    Name_Archivo=object()

    #Archivo Fuente
    File=object()

    #BOTONES
    Compilar=object()
    ## OBJETIOS

    Scan=object()
    def __init__(self,n,m):
        #Parametros de la ventana
        self.ventana=Tk()

        self.tx=n
        self.ty=m
        
        tm=str(self.tx)+'x'+str(self.ty)
        self.ventana.title('Compilador MC68HC11') 
        self.ventana.configure(background='#ecf0f1')
        self.ventana.resizable(False, False)
        self.ventana.geometry(tm)
        #### CONFIGURACION MENU ######
        self.Menu=Menu(self.ventana)
        self.ventana.config(menu=self.Menu)
        ###CONFIGURACION SUBMENU
        #ARCHIVO
        self.FileMenu=Menu(self.Menu)
        self.Menu.add_cascade(label='Archivo',menu=self.FileMenu)
        self.FileMenu.add_command(label='Abrir Archivo',command=self.AbrirArchivo)
        #SEPARADOR
        self.FileMenu.add_separator()
        self.FileMenu.add_command(label='Salir',command=self.ventana.destroy)
        #CONFIG
        self.ConfigMenu=Menu(self.Menu)
        self.Menu.add_cascade(label='Configuracion',menu=self.ConfigMenu)
        self.ConfigMenu.add_command(label='Configurar Preferencias',command=self.Config)  
        #AYUDA
        self.Help=Menu(self.Menu)
        self.Menu.add_cascade(label='Ayuda',menu=self.Help)
        self.Help.add_command(label='Acerca De..',command=self.Ayuda)
        
        self.Name_Archivo = StringVar()
        self.Name_Archivo.set('Archivo')
        ## TEXT HOLDER ####
        self.TextHolderM()
        self.ErrorHolderM()
        #self.TextHolder()
        Archivo=Label(self.ventana,textvariable=self.Name_Archivo,font=("Helvetica", 10))
        Archivo.place(x=50,y=10)
        #COMPILAR
        self.Compilar=Button(self.ventana,text='Compilar',command=self.Compilar)
        self.Compilar.place(x=175,y=5)
        #ERRORES
        Err=Label(self.ventana,text='Compilacion',font=("Helvetica", 10))
        Err.place(x=50,y=500)

    def Compilar(self):
        if self.FilePath=='':
            messagebox.showerror('ERROR','NO HAY NINGUN ARCHIVO PARA COMPILAR')
            return
        self.Scan=Scanner(self.FilePath,Table,error_list,saltos,html)
        self.Scan.run()
        self.ErrorHolder.delete('1.0', END)
        self.ErrorHolder.insert(INSERT, self.Scan.S_errores)
        self.TextHolder.delete('1.0', END)
        
        path=self.Scan.archivolst
        print(path)
        try:
           File=open(path,'r')
        except:
            messagebox.showerror('ERROR','ERROR AL ABRIR EL ARCHIVO')
            return
        for linea in File:
            self.TextHolder.insert(INSERT, linea)        
        return
    def Ayuda(self):
        Info='Este programa en su totalidad por Miguel Angel López Soto Alias "ElJorseman"\n'
        Info+='Cualquier duda,sugerencia o comentario es bien recibida para seguir mejorando\n'
        Info+='Puse esto porque estaba aburrido y me gustan los Easter Eggs xD\n'
        Info+='Ya no se que mas poner asi que le deseo suerte extraño que esta usando mi programa :)\n'
        print(Info)
        messagebox.showinfo("Acerca De",Info)
        return
    def Config(self):
        
        return
    def AbrirArchivo(self):
        self.ErrorHolder.delete('1.0', END)
        self.TextHolder.delete('1.0', END)
        self.FilePath=filedialog.askopenfilename(filetypes = (("ASC File","*.asc"),("All Files","*.*")) )
        try:
           self.File=open(self.FilePath,'r')
        except:
            messagebox.showerror('ERROR','ERROR AL ABRIR EL ARCHIVO')
            return
        name=self.getName(self.FilePath)
        self.Name_Archivo.set(name)
        for linea in self.File:
            self.TextHolder.insert(INSERT, linea)
        return
    def Buscar(self):
        return
    def getName(self,path):
        k=path.rindex('/')
        print(path[:k+1])
        return path[k+1:]
    def TextHolderM(self):
        self.TextHolder=Text(self.ventana,width=100,height=25,wrap=NONE,font='Courier 11')
        self.TextHolder.place(x=50,y=50)
        
        S=Scrollbar(self.ventana,orient='vertical' ,command=self.TextHolder.yview)
        S.pack(side=RIGHT,fill=Y)
        self.TextHolder.configure(yscrollcommand=S.set)

        Sx=Scrollbar(self.ventana,orient='horizontal' ,command=self.TextHolder.xview)
        Sx.pack(side=BOTTOM,fill=X)
        
        self.TextHolder.configure(xscrollcommand=S.set)
        #self.Name_Archivo=Title
    def ErrorHolderM(self):
        self.ErrorHolder=Text(self.ventana,width=100,height=7,wrap=NONE,font='Courier 11')
        self.ErrorHolder.place(x=50,y=550)
        return
    def run(self):
        self.ventana.mainloop()
        return



def main():

    Root=Ventana(1000,700)
    Root.run()
    
    return

main()
