from tkinter import *
from TablaSimbolos import *
from Comm import *
from Files import *
from OpString import *
from EtiqVar import *
from Mnem import *
from tkinter import messagebox
import math

class Scanner:
    #ARCHIVO FUENTE
    archivo=object()
    n_lines=int()
    lines=list()
    nombre=''
    archivolst=''
    archivohex=''
    archivohtml=''
    ##VARIABLES FORMATO
    i=0
    ns=17
    Tabla_Simbolos=object()
    S_errores=''
    #LISTAS
    ListErrors=list()
    ListLabels=dict()
    ListVars=dict()
    ListCF=list()
    ListCFC=list()
    ListCO=list()
    #Pila Hexadecimal
    ListHex=list()
    ListCal=dict()
    ListMemCalc=list()
    
    #Simbolos Clave Compilacion
    SimbolComment='*'
    SimbolsMnem=[' ','\t','\n']
    ##Palabras Reservadas
    Var='EQU'
    Inicio='ORG'
    Fin='END'
    FCB='FCB'
    line=''
    NemSpecial=['BCLR','BSET']
    NemSpecialS=['BRCLR','BRSET']
    #Variables ORG y END
    containsBegin=False
    containsEnd=False
    containsCalc=False
    containsErrors=False
    #Inicio Memoria
    ORG=dict()
    OrgMain=hex(0)
    Saltos=list()
    InM=int()
    def __init__(self,nombre_archivo,Table,error_list,saltos,html):
        self.nombre=nombre_archivo
        self.archivohtml=html
        try:
            self.archivo=open(nombre_archivo,'r')
        except:
            messagebox.showerror('ERROR','ERROR AL ABRIR EL ARCHIVO FUENTE')
            return
        self.n_lines=len(self.archivo.readlines())
        try:
            self.lines=open(nombre_archivo,'r').readlines()
        except:
            messagebox.showerror('ERROR','ERROR AL ABRIR EL ARCHIVO FUENTE')
        self.Tabla_Simbolos=Table
        self.Errores=ListFromFile(error_list)
        self.Saltos=ListFromFile(saltos)
        print(self.Saltos)
        self.ini_list()
        return
    def clearAll(self):
        self.ListErrors.clear()
        self.ListCF.clear()
        self.ListCFC.clear()
        self.ListCO.clear()
        
        self.ListHex.clear()
        
        self.ListLabels.clear()
        self.ListVars.clear()
        self.ORG.clear()

        self.ListCal.clear()
        self.ListMemCalc.clear()  
        return
    def ini_list(self):
        self.clearAll()
        self.ListErrors.append('ERRORES')
        for i in range(self.n_lines):
            #self.ListErrors.append(list())
            self.ListCF.append('')
            self.ListCFC.append('')
            self.ListHex.append('')
            self.ListMemCalc.append(hex(0))
        return
    
    def run(self):
        #self.setLabelList()
        i=0
        for linea in self.lines:
            s=''
            com=''
            s=linea
            if containsComm(linea):
                s,com=getStringComm(linea.strip('\n'))
            if isEmptyLine(linea) or is_Comment(linea):
                self.toFormatSC('NOC',None,None,None,None,linea.strip('\n'),i)
                i+=1
                continue
            if isEnd(s):
                self.OrgMain=list(self.ORG.keys())[0]
                self.toFormatSC('NOC',None,None,None,None,linea.strip('\n'),i)
                self.containsEnd=True
                break
            if isLab(s):
                self.LabelProcess(s,com,i)
                i+=1
                continue
            if isVar(s):
                self.varProcess(s,com,i)
                i+=1
                continue
            if not isLab(linea):
                if isInicio(s):
                    print('Inicio')
                    self.InicioProcess(s,com,i)
                    i+=1
                    continue
                #elif isEnd(s):
                    #self.EndProcess(s,com,i)
                #    continue
                else:
                    self.MnemonicosProcess(s,com,i)

                    
            i+=1

        if self.containsCalc:
            self.CalcSaltos()
        
        for i in self.ListCF:
            print(i)
            #pass
        if not self.containsEnd:
            self.ListErrors.append(self.Errores[9])
        archivo,self.archivolst=self.genFile('w',self.ListCF,self.nombre,'.LST')
        
        if not self.containsErrors :
            self.printHex()
            self.ListErrors.append('0 :)')
            otro,self.archivohex=self.genFile('w',self.ListCO,self.nombre,'.HEX')
        
        self.S_errores,self.archivolst=self.genFile('a+',self.ListErrors,self.nombre,'.LST')
        #CREA EL HMTL
        try:
            html=open(self.archivohtml,'r')
        except:
            print('Error :(')
        inihtml=''
        for linea in html:
            inihtml+=linea
        self.ListCFC.insert(0,inihtml)
        self.ListCFC.append('<span class="oper">'+self.S_errores+'</span>')
        self.ListCFC.append('</body>'+'</html>')
        self.genFile('w',self.ListCFC,self.nombre,'.HTML')
        print(self.S_errores)
        
        return
    
    def genFile(self,Mode,List,Path,Ext):
        s=''
        path=''
        name=path

        if '/' in Path:
            name=getName(Path)
            path=getPath(Path)
            
        if '.' in name:
            i=name.index('.')
            name=name[:i]
            
        File=path+name+Ext
        f = open (File,Mode)
        #print(List)
        for i in List:
            s+=i+'\n'
            f.write(i+'\n')
        f.close() 
        return s,File
    def printWithFormat(self,LHex,Mem):
        n=len(LHex)
        #print(LHex)
        c=int(n/16)
        M=int(str(Mem),16)
        mod=n%16
        print(mod)
        for i in range(c):
            s=''
            M=str(hex(M))[2:].upper()
            s='<{}>'.format(M)
            for j in range(i*16,i*16+16):
                s+=' ' + LHex[j]
            print(s)
            self.ListCO.append(s)
            M=int(M,16)+16
        M=str(hex(M))[2:].upper()
        s='<{}>'.format(M)        
        for k in range(c*16,n):
            s+=' ' + LHex[k]
        for o in range(16-mod):
            s+=' ' + 'FF'
        self.ListCO.append(s)
        print(s)   
        return
    def printHex(self):
        MemIn=str(self.OrgMain)[2:]
        LHex=list()
        for i in self.ListHex:
            if i=='':
                continue
            n=len(i)
            for j in range(2,n+1,2):
                LHex.append(i[j-2:j])
        
        self.printWithFormat(LHex,MemIn)   
        return
    def CalcSaltos(self):
        items=list(self.ListCal.keys())
    
        for linea in items:
            s=''
            com=''
            s=linea
            i=self.ListCal[linea]
            if containsComm(linea):
                s,com=getStringComm(linea)
            Data=getDataFromLineNem(s)
            if self.isDirMode(Data[0],'REL'):
                self.CalcS('REL',Data,s,com,i)
                continue
            if self.isDirMode(Data[0],'EXT'):
                self.CalcS('EXT',Data,s,com,i)
                continue
            if Data[0] in self.NemSpecialS:
                self.SpecialProcess(Data,s,com,i)
                            
        return

    def SpecialOperProcess(self,linea,Data,i):
        oper=Data[1].split(',')
        typ=oper[1]
        
        Dir,uno,dos=self.getDirOperSpecial(typ,oper)
        
        op1=self.getOper(uno,'VAR',linea,i)
        op2=self.getOper(dos,'VAR',linea,i)
        
        return Dir,op1,op2
    def SpecialProcess(self,Data,s,com,i):
        n=len(Data)
        linea=s+com
        labels=list(self.ListLabels.keys())
        
        if n==3:
            if Data[2] in labels:
                n_label=self.ListLabels[Data[2]]
                Dir,op1,op2=self.SpecialOperProcess(s,Data,i)
                operL=self.getSalto(Data,Dir,i,n_label)
                if operL is None:
                    #ERROR
                    self.Error(8,linea,i)
                    return
                if op1 is None or op2 is None:
                    ##ERROR
                    self.Error(7,linea,i)
                    return
                
                operL=operL.upper()
                
                OpCode=self.getOPCode(Data[0],Dir)
                n_bytes=self.getNumByte(Data[0],Dir)
                
                Oper=op1+op2+operL
                MemStr=self.ListMemCalc[i][2:].upper()
                
                if self.lenOperValid(Oper,OpCode,n_bytes):
                    Oper=AdjustOper(Oper,OpCode,n_bytes)
                    ###### COMPILA ESPECIALES #######
                    self.printCalc(i,MemStr,OpCode,Oper,s,Data,Data[2]+' '+com)
                    return
                else:
                    self.Error(7,linea,i)
                    return                

                
                
            else:
                self.Error(3,linea,i)
                return
        else:
            self.Error(11,linea,i)
            return

    
    def printCalc(self,i,MemStr,OpCode,Oper,s,Data,com):
        Nl=str(len(str(self.n_lines)))
        s='{:0{NL}}{}{}({}{})'.format(i,':',MemStr,OpCode,Oper,NL=Nl)
        s='{:20}:\t{:6}{:<10}\t{}'.format(s,Data[0],Data[1],com)
        self.printCalColor(i,MemStr,OpCode,Oper,s,Data,com)
        #print(s)
        self.ListCF[i]=s
        self.ListHex[i]=OpCode+Oper
        return

    def printCalColor(self,i,MemStr,OpCode,Oper,s,Data,com):
        
        spanNem='<span class="nem">'
        
        spanComm='<span class="comm">'

        spanOper='<span class="oper">'
 
        spanFin='</span>'
        
        pin='<p class="text">'
        pfin='</p>'
        
        Nl=str(len(str(self.n_lines)))
        s=pin+'{:0{NL}}{}{}({}{})'.format(i,':',MemStr,OpCode,Oper,NL=Nl)
        s='{:20}:{:6}{:<10}{}'.format(s,spanNem+Data[0]+spanFin,spanOper+Data[1]+spanFin,spanComm+com+spanFin+pfin) #+'<br/>')
        self.ListCFC[i]=s
        return
    def CalcS(self,Mode,Data,s,com,i):
        n=len(Data)
        linea=s+com
        labels=list(self.ListLabels.keys())
        
        if n==2:
            if Data[1] in labels:
                n_label=self.ListLabels[Data[1]]
                #print(Data)
                oper=self.getSalto(Data,Mode,i,n_label)
                if oper == None:
                    self.Error(8,linea.strip('\n'),i)
                    return
                #print(oper)
                oper=oper.upper()
                MemStr=self.ListMemCalc[i][2:].upper()
                
                OpCode=self.getOPCode(Data[0],Mode)
                n_bytes=self.getNumByte(Data[0],Mode)
                
                if self.lenOperValid(oper,OpCode,n_bytes):
                    oper=AdjustOper(oper,OpCode,n_bytes)
                    ###### COMPILA RELATIVO #######
                    self.printCalc(i,MemStr,OpCode,oper,s,Data,com)
                    return
                else:
                    self.Error(7,linea,i)
                    return
            else:
                self.Error(3,linea,i)
                return
        else:
            self.Error(11,linea,i)
        return
    
    def getSalto(self,Data,Mode,i,n_label):
        n=int(((i-n_label)/(abs(i-n_label)))*(-1))
        #print(self.ListMemCalc)
        ini=self.ListMemCalc[i]
        j=0
        fin=hex(0)
        while(fin==hex(0)):
            fin=self.ListMemCalc[n_label+j]
            j+=1

        delta=abs( int(fin,16) - int(ini,16))

        n_bytes=self.getNumByte(Data[0],Mode)
        ##### VALIDACIONES #######
        if Mode=='REL' or Mode=='DIR' or Mode=='IND,X' or Mode=='IND,Y':
            if delta*n>=-128 and delta*n<=127: 
                if n>0:
                    op=int(str(delta),16)-int(str(n_bytes),16)
                    op=hex(op)[2:]
                    return op
                else:
                    op=compA2(delta+n_bytes)
                    return op[2:]
            else:
                #### ERROR SALTO RELATIVO ###
                return None
        elif Mode=='EXT':
            return fin[2:]
        else:
            print('Hola :)')
        return
    
    def MnemonicosProcess(self,s,com,i):
        linea=s+com
        Data=getDataFromLineNem(s)
        if self.inMnemonicos(Data[0]):
            ## REVISAMOS SI ES LA DIRECTIVA FCB
            if Data[0] == self.FCB:
                linea='\t'+removeSpace(linea)
                self.toFormatSC('NOC',None,None,None,None,linea,i)
                return
            ### REVISAMOS SI ES INHERENTE #######   
            if self.isDirMode(Data[0],'INH'):
                self.INHProcess(Data,linea,com,i)
                return
            ### ERROR 5 INSTRUCCIÓN CARECE DE OPERANDO(S) #####
            if len(Data)==1:
                self.Error(5,linea,i)
                return
            ## REVISAMOS SI ES RELATIVO ##
            if self.isDirMode(Data[0],'REL'):
                self.containsCalc=True
                self.RelProcess(Data,linea,i)
                return
            ## REVISAMOS SI ES INMEDIATO ##
            if self.isDirMode(Data[0],'IMM') and '#'==Data[1][0]:
                self.IMMProcess(Data,linea,com,i)
                return               
            if self.isDirMode(Data[0],'IND,X') or self.isDirMode(Data[0],'IND,Y'):
                    if ',' in Data[1] and ( 'X' in Data[1].upper() or  'Y' in Data[1].upper() ):
                        self.INDProcess(Data,linea,com,i)
                        return
                    if self.isDirMode(Data[0],'DIR'):
                        self.DirProcess('DIR',Data,linea,com,i)
                        return
                    if self.isDirMode(Data[0],'EXT'):
                        self.DirProcess('EXT',Data,linea,com,i)
                        return
            return           
        else:
            ## ERROR 004 MNEMÓNICO INEXISTENTE ##
            self.Error(4,linea,i)
            return
        return

    def DirProcess(self,Mode,Data,linea,com,i):
        if Data[0] in self.Saltos:
            #print('CALCULAR SALTO')
            self.containsCalc=True
            linea=removeSpace(linea)
            self.ListCal[linea]=i
            if Data[0].upper()=='JSR':
                Mode='EXT'
            #print('Compilacion en segunda vuelta') 
            n_bytes=self.getNumByte(Data[0],Mode)
            self.toFormatSC('NOC',None,None,None,n_bytes,linea,i)
            return
        if Data[0] in self.NemSpecial:
            self.CompSpecial(Data,linea,com,i)
            return
        oper=Data[1]
        oper=self.getOper(oper,'VAR',linea,i)
        if oper is None:
            return
        OpCode=self.getOPCode(Data[0],Mode)
        n_bytes=self.getNumByte(Data[0],Mode)
        
        if self.lenOperValid(oper,OpCode,n_bytes):
            #VALIDO PARA COMPILAR DIRECTO ##
            oper=AdjustOper(oper,OpCode,n_bytes)
            self.toFormatSC(Mode,Data,OpCode,oper,n_bytes,com,i)
            return   
        else:
            self.DirProcess('EXT',Data,linea,com,i)
            return
        return
    def RelProcess(self,Data,linea,i):
        if Data[0].upper() in self.Saltos:
            linea=removeSpace(linea)
            self.ListCal[linea]=i
            #print('Compilacion en segunda vuelta')
            n_bytes=self.getNumByte(Data[0],'REL')
            self.toFormatSC('NOC',None,None,None,n_bytes,linea,i)
            return
        print('Algo Anda mal .....')
        self.toFormatSC('NOC',None,None,None,None,linea,i)
        return
    def getDirOperSpecial(self,typ,oper):
        Dir='IND,'
        if typ.upper()=='X':
            Dir+='X'
            uno=oper[0]
            dos=oper[2]
        elif typ.upper()=='Y':
            Dir+='Y'
            uno=oper[0]
            dos=oper[2]
        else:
            ## COMPILAR DIRECTO
            Dir='DIR'
            uno=oper[0]
            dos=oper[1]

        if '#' == uno[0]:
            uno=uno[1:]
        if '#' == dos[0]:
            dos=dos[1:]
            
        return Dir,uno,dos
    def CompSpecial(self,Data,linea,com,i):
        
        Dir,op1,op2=self.SpecialOperProcess(linea,Data,i)
        
        OpCode=self.getOPCode(Data[0],Dir)
        n_bytes=self.getNumByte(Data[0],Dir)
        
        if op1 is None or op2 is None:
            self.Error(12,linea,i)
            return
        else:
            oper=op1+op2
            if self.lenOperValid(oper,OpCode,n_bytes):
                oper=AdjustOper(oper,OpCode,n_bytes)
                ###### COMPILA INDEXADO #######
                self.toFormatSC(Dir,Data,OpCode,oper,n_bytes,com,i)
                return
            else:
                self.Error(7,linea,i)
                return
        return
    def getTypeIND(self,oper):
        typ=oper[1]
        Dir='IND,'
        if typ.upper()=='X':
            Dir+='X'
        elif typ.upper()=='Y':
            Dir+='Y'
        else:
            self.Error(11,linea,i)
            return None
        return Dir
    
    def INDProcess(self,Data,linea,com,i):
        oper=Data[1].split(',')
        
        if Data[0] in self.Saltos:
            linea=removeSpace(linea)
            self.ListCal[linea]=i
            #print('Compilacion en segunda vuelta')
            Dir=self.getTypeIND(oper)
            n_bytes=self.getNumByte(Data[0],Dir)
            self.toFormatSC('NOC',None,None,None,n_bytes,linea,i)
            return
        
        if Data[0].upper() in self.NemSpecial and len(oper)==3:
            self.CompSpecial(Data,linea,com,i)
            return
        Dir=self.getTypeIND(oper)
        if Dir is None:
            return
        
        OpCode=self.getOPCode(Data[0],Dir)
        n_bytes=self.getNumByte(Data[0],Dir)
        op=self.getOper(oper[0],'VAR',linea,i)
        
        if op is None:
            self.Error(12,linea,i)
            return
        else:
            if self.lenOperValid(op,OpCode,n_bytes):
                oper=AdjustOper(op,OpCode,n_bytes)
                ###### COMPILA INDEXADO #######
                self.toFormatSC(Dir,Data,OpCode,oper,n_bytes,com,i)
                return
            else:
                self.Error(7,linea,i)
                return
        return
    def IMMProcess(self,Data,linea,com,i):
        if Data[1][0]=='#':
            oper=Data[1][1:]
            op=self.getOper(oper,'VAR',linea,i)
            
            OpCode=self.getOPCode(Data[0],'IMM')
            n_bytes=self.getNumByte(Data[0],'IMM')
            
            if op is None:
                self.toFormatSC('NOC',None,None,None,None,linea,i)
                return
            else:
                if self.lenOperValid(op,OpCode,n_bytes):
                    oper=AdjustOper(op,OpCode,n_bytes)
                    ###### COMPILA INMEDIATO #######
                    #print('Compila Inmediato')
                    #print(Data)
                    self.toFormatSC('IMM',Data,OpCode,oper,n_bytes,com,i)
                    return
                else:
                    self.Error(7,linea,i)
                    return
                    
        else:
            self.Error(11,linea,i)
        return

    def INHProcess(self,Data,linea,com,i):
        if len(Data)==1:
            ## COMPILAR INHERENTE ##
            OpCode=self.getOPCode(Data[0],'INH')
            N_bytes=self.getNumByte(Data[0],'INH')
            if N_bytes is not -1:
                self.toFormatSC('INH',Data,OpCode,None,N_bytes,com,i)
            return
        else:
            self.Error(6,linea,i)
            return

    def isDirMode(self,Nem,Dir):
        listnem=list(self.Tabla_Simbolos.Mnemonicos)
        i=listnem.index(Nem.lower())
        if self.Tabla_Simbolos.DirModes[Dir][0][i].isalnum():
            #print('Es ',Dir)
            return True
        return False
    def lenOperValid(self,oper,nem,n_bytes):
        n=len(oper)
        m=len(nem)
        n_opor=math.ceil(n/2)
        n_nem=math.ceil(m/2)
        if n_opor <= (n_bytes-n_nem):
            return True
        return False
    def getOper(self,oper,Mode,linea,i):
        Vars=list(self.ListVars.keys())
        Lab=list(self.ListLabels.keys())
        if oper[0]=='$':
            try:
                op=int(oper[1:],16)
                op=hex(op)
                #print(oper[1:])
                return str(op[2:])
            except ValueError:
                self.Error(12,linea,i)
                return
        if oper.isdigit():
            try:
                dec=hex(int(oper,10))
                #print(dec[2:])
                return dec[2:]
            except ValueError:
                self.Error(12,linea,i)
                return
        if oper[0]=="'":
            if len(oper)==2:     
                try:
                    asccii=ord(oper[1])
                    op=hex(asccii)
                    #print(op[2:])
                    return op[2:]
                except ValueError:
                    self.Error(11,linea,i)
                    return
            else:
                self.Error(7,linea,i)
                return
        if Mode=='VAR':
            if oper in Vars:
                value=self.ListVars[oper]
                op=self.getOper('$'+value,Mode,linea,i)
                return op
            else:
                self.Error(1,linea,i)
                self.Error(2,linea,i)
                return         
        if Mode=='LAB':
            if oper in Lab:
                #### CALCULO DE ESAS WEAS :V
                #Value=self.ListVars[oper]
                return
            else:
                self.Error(3,linea,i)
                return
        return

    def EndProcess(self,s,comm,i):
        linea=s+comm
        Data=getDataFromLine(s,self.Fin)
        if Data[0]=='':
            #end=hex(int(oper,16))
            self.containsEnd=True
            self.OrgMain=self.ORG[0]
            linea='\t'+removeSpace(linea)
            self.toFormatSC('NOC',None,None,None,None,linea,i)
            """
            oper=operNumber(Data[1])
            if isOperValid(oper):
                ##### END VALIDO ###################
                end=hex(int(oper,16))
                #print(self.ORG)
                if end in self.ORG.keys():
                    self.containsEnd=True
                    self.OrgMain=end
                    linea='\t'+removeSpace(linea)
                    self.toFormatSC('NOC',None,None,None,None,linea,i)
                else:
                    ##### ERROR 14 END ###################
                    self.Error(14,linea,i)
                return
            else:
                ##### ERROR 12 ###################
                self.Error(12,linea,i)
            """
        else:
            ####### ERROR 11 SINTAXIS ##########
            self.Error(11,linea,i)
        return
    
    def InicioProcess(self,s,comm,i):
        linea=s+comm
        Data=getDataFromLine(s,Inicio)
        if Data[0]=='':
            oper=operNumber(Data[1])
            if isOperValid(oper):
                ##### ORG VALIDO ###################
                self.ORG[hex(int(oper,16))]=i
                self.InM=int(oper,16)
                #self.ListHex[i]='ORG'
                self.containsBegin=True
                linea='\t'+removeSpace(linea)
                print(linea)
                self.toFormatSC('NOC',None,None,None,None,linea,i)
                return
            else:
                ##### ERROR 12 ###################
                self.Error(12,linea,i)                
        else:
            ####### ERROR 11 SINTAXIS ##########
            self.Error(11,linea,i) 
        return
    def varProcess(self,s,comm,i):
        linea=s+comm
        #print(linea)
        Data=getDataFromLine(s,self.Var)
        oper=operNumber(Data[1])
        if nameIsValid(Data[0]):
            if isOperValid(oper):
                self.ListVars[Data[0]]=oper
                ####### VARIABLE VERIFICADA ##########
                linea=linea.strip('\n')
                self.toFormatSC('NOC',None,None,None,None,linea,i)
                return
            else:
                ##### ERROR 12 ###################
                self.Error(12,linea,i)
                return
        else:
            ##### ERROR 13 ###################
            self.Error(13,linea,i)
        return                
    def inMnemonicos(self,nem):
        Lm=list(self.Tabla_Simbolos.Mnemonicos)
        Lm.append(self.FCB.lower())
        if nem.lower() in Lm:
            return True
        return False
    def printLabel(self,lab,com,i):
        linea=lab+com  
        lab=lab.strip()
        lab=lab.strip('\n')
        lab=lab.strip('\t')
        self.ListLabels[lab]=i
        linea=lab+com
        linea=linea.strip('\n')
        self.toFormatSC('NOC',None,None,None,None,linea,i)        
        return
    def LabelProcess(self,s,com,i):
        Lm=list(self.Tabla_Simbolos.Mnemonicos)
        Lm.append(self.FCB.lower())
        lab=s
        linea=s+com
        for nem in Lm:
            if nem in s.lower():
                #print('No se que hacer :v')
                Data=getDataFromLineNem(s)
                if len(Data)==1:
                    break
                if len(Data)==2:
                    if Data[1].lower()==nem:
                        self.MnemonicosProcess(nem.upper(),com,i)
                        return
                    else:
                        ##### ERROR 9###################
                        self.Error(9,linea,i)
                        return
                if len(Data)==3:
                    lab=Data[0]
                    ## ANALIZAR MNEMONICO DESPUES DE LABEL
                    self.printLabel(lab,com,i)
                    self.MnemonicosProcess(nem.upper()+' '+Data[2],com,i)
                    return
        self.printLabel(lab,com,i)
        return
    
    def toFormatColor(self,DIR,Data,OpCode,Oper,N_bytes,MemStr,com,i):
        s=''
        ##FORMATO HTML CSS
        spanNoc='<span class="noc">'
        
        spanNem='<span class="nem">'
        
        spanComm='<span class="comm">'

        spanOper='<span class="oper">'
 
        spanFin='</span>'
        
        pin='<p class="text">'
        pfin='</p>'

        Nl=str(len(str(self.n_lines)))
        if DIR=='NOC':
            s=pin+'{:0{NL}}:'.format(i,NL=Nl)+spanNoc+com+spanFin+pfin#+'<br/>'
            self.ListCFC[i]=s
            if N_bytes is None:
                return
            return

        OpCode=OpCode.upper()
        
        if DIR=='INH':
            s=pin+'{:0{NL}}{}{}({}{})'.format(i,':',MemStr,OpCode,'',NL=Nl)
            s='{:20}:{:6}{:>10}{}'.format(s,spanNem+Data[0]+spanFin,'',spanComm+com+spanFin+pfin)#+'<br/>')
            self.ListCFC[i]=s
            return
        Oper=Oper.upper()
        
        s=pin+'{:0{NL}}{}{}({}{})'.format(i,':',MemStr,OpCode,Oper,NL=Nl)
        s='{:20}:{:6}{:<10}{}'.format(s,spanNem+Data[0]+spanFin,spanOper+Data[1]+spanFin,spanComm+com+spanFin+pfin)#+'<br/>')
        self.ListCFC[i]=s
        
        return     
    
    def toFormatSC(self,DIR,Data,OpCode,Oper,N_bytes,com,i):
        s=''
        Nl=str(len(str(self.n_lines)))
        if DIR=='NOC':
            s='{:0{NL}}:'.format(i,NL=Nl)+' '*self.ns+ com
            #print(s)
            self.ListCF[i]=s
            self.toFormatColor(DIR,Data,OpCode,Oper,N_bytes,'',com,i)
            if N_bytes is None:
                #print(s)
                return
            self.ListMemCalc[i]=hex(self.InM)
            self.InM+=N_bytes
            return
        ## MEMORIA ####
        try:
            ndir=self.InM
            Mem=hex(ndir)
            MemStr=str(Mem)[2:].upper()
        except IndexError as e:
            ## ERROR 15 ###########
            self.Error(15,linea,i)        
            return
        OpCode=OpCode.upper()
        
        if DIR=='INH':
            #print('Imprime INH')
            s='{:0{NL}}{}{}({}{})'.format(i,':',MemStr,OpCode,'',NL=Nl)
            s='{:20}:\t{:6}{:>10}\t{}'.format(s,Data[0],'',com)
            self.ListCF[i]=s
            self.toFormatColor(DIR,Data,OpCode,Oper,N_bytes,MemStr,com,i)
            self.ListMemCalc[i]=hex(self.InM)
            self.InM+=N_bytes
            self.ListHex[i]=OpCode
            #print(s)
            return
        Oper=Oper.upper()
        
        #print('Compila NEM')
        
        s='{:0{NL}}{}{}({}{})'.format(i,':',MemStr,OpCode,Oper,NL=Nl)
        s='{:20}:\t{:6}{:<10}\t{}'.format(s,Data[0],Data[1],com)
        self.ListCF[i]=s
        self.toFormatColor(DIR,Data,OpCode,Oper,N_bytes,MemStr,com,i)
        self.ListMemCalc[i]=hex(self.InM)
        self.InM+=N_bytes
        self.ListHex[i]=OpCode+Oper
        #print(s)           
        return


    
    def getOPCode(self,Mnem,Dir):
        listnem=list(self.Tabla_Simbolos.Mnemonicos)
        i=listnem.index(Mnem.lower())
        op=self.Tabla_Simbolos.DirModes[Dir][0][i]
        #print(listnem[i],'====',op)
        return op
    def getNumByte(self,Mnem,Dir):
        listnem=list(self.Tabla_Simbolos.Mnemonicos)
        i=listnem.index(Mnem.lower())
        n=self.Tabla_Simbolos.DirModes[Dir][1][i]
        #print(listnem[i],'====',n)
        try:
            m=int(n)
            return m
        except ValueError as e:
            print(e)
            return -1

    def Error(self,n,linea,i):
        print(self.Errores[n-1])
        print(linea)
        self.containsErrors=True
        self.toFormatSC('NOC',None,None,None,None,linea,i)
        self.ListErrors.append(str(i)+' : '+self.Errores[n-1])    
        return
