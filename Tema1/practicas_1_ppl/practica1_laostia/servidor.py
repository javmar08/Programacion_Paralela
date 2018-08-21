# -*- coding: utf-8 -*-
"""

@author: Diego Fernández López
"""
from multiprocessing.connection import Listener
from time import sleep
from multiprocessing import Process,Manager,Condition
def print_(a,b=''):
    print b,a
    return a
class kernel:
    """
    Guarda la estructura con la imformacion referente al
    listener
    """
    def __init__(self,dim_i=3,dim_j=1):
        self.jugadores=[]
        self.M=Manager()
        self.listenner=Listener(address=('localhost',6000),authkey='secret password')
        self.color=0
        
        self.numCasillas=0
        self.numEspera=self.M.list([0,0,self.numCasillas])
        self.desocupado=Condition()      
        self.cont=0
        self.turno=self.M.list([0])
        self.dim_i=dim_i
        self.dim_j=dim_j
        self.len=self.dim_i*self.dim_j
        self.tablero=(self.M.list([0]*(self.dim_i*self.dim_j)))

    def trhows(self):
        '''
        lanza los programas iniciando el listenner
           accion
           carga_nuevos_jugadores
        '''
        CNP=Process(target=self.carga_nuevos_jugadores)
        
        
        CNP.start();CNP.join()
    def carga_nuevos_jugadores(self):
        print 'carga up'        
        while self.numCasillas<self.len:
            new_con=self.listenner.accept()
            self.jugadores.append(new_con)
            new_con.send((self.color,(self.dim_i,self.dim_j)))
            P=Process(target=self.check,args=(new_con,self.color))
            (self.color,self.cont)=(1-self.color,self.cont+1)
            print 'pass'
            P.start()
            print 'pass2'
    def check(self,con,color):
            '''
        Controla el I/O de un jugador
        print 'check up'
            '''
            cont=True
            while cont and self.numCasillas<self.len:
                print 'esperando para colocar'
                recibido=print_(con.recv())
                if recibido!='q':
                    cont2=True
                    while cont2:
                        if self.desocupado.acquire():
                            R=self.protocol(recibido)
                            self.desocupado.notify_all()
                            self.desocupado.release()
                            con.send(R)
                            
                            if R[0]==2:
                                sleep(1.0)
                                con.send(R)
                            cont2=False
                        else:
                            self.numEspera[color]+=1
                            print 'pacientes:', self.numEspera
                            self.desocupado.notify_all()
                            self.desocupado.release()
                            self.desocupado.wait()
                            self.numEspera[color]-=1
                else:
                    con.close()
                    cont=False
            
    def protocol(self,recibido):
        
        if (recibido[0]==self.turno[0]) or (self.numEspera[1-self.turno[0]]==0): #self.desocupado.acquire():
            if (self.tablero[(recibido[1])])==0:
                self.turno[0]=1-recibido[0]
                self.tablero[(recibido[1])]=recibido[0]+1
                self.numEspera[2]+=1
                Ans=(1,self.dim_i,self.dim_j,self.tablero[:])
                
            else:
                
                Ans=(2,self.dim_i,self.dim_j,self.tablero[:])
           
            
            
        else:
             Ans= (0,self.dim_i,self.dim_j,self.tablero[:])
        
        if self.numEspera[2]==len(self.tablero):
             Ans=(3,self.dim_i,self.dim_j,self.tablero[:])
        return Ans
from Tkinter import *

class interface:
    
    def __init__(self,color,dim_i,dim_j,colaIn,colaOut):
        self.colaIn=colaIn 
        self.colaOut=(colaOut)
        self.colaIn=colaIn
        self.v0=Tk()
        if color:
            title='Equipo Rojo'
        else:
            title='Equipo Azul'
        self.v0.title(title)
        self.v0.resizable(0,0)
        self.color,self.nl,self.matriz,self.ganador=color,[],[0]*(dim_i*dim_j),[0]
        self.finalizado=False
        ind=0
        self.dim_i,self.dim_j=(dim_i,dim_j)
        self.nl=[]
        c1,c2=0,0
        print dim_i,dim_j
        while ind < dim_i*dim_j:
            self.nl.append(Button(self.v0,text="",width=10,height=5,bg="white"))
            self.nl[ind].grid(row=c2,column=c1)
            print c1,c2
            ind+=1
            if c1==dim_i-1:(c1,c2)=(0,c2+1)
            else: c1+=1
        
        
        i=0
        a=[1]
        while i <(self.dim_i*self.dim_j):
            j=i+0
            a[0]=j
            AcB=accion_boton(i,self.jugar)
            self.nl[i].config(command= AcB)
            i=i+1

        
        
        

    
    
    
    
    def limpiar_botones(self):
        color="white"
        ind,largo=0,len(nl)
        while ind < largo:
            self.nl[ind].config(bg=color)
            ind+=1
        self.matriz[:]=0
    
    def declarar_ganador(self):
        Mios=len(filter(lambda x:x==self.color+1,self.matriz))
        Adversario=(1-self.color)+1
        Suyos=len(filter(lambda x:x==Adversario,self.matriz))
        return Mios-Suyos
    def raises(self,R):
        v1=Tk()
        
        v1.title("")
        v1.resizable(0,0)
        print 'R' ,R
        if R>0:texto='ganaste'
        elif R<0:texto='perdiste'
        else:texto='empataste'
        l1=Label(v1,text=texto)
        l1.pack()
        v1.update()

    def jugar(self,posicion):
        print 'juagada',posicion
        print 'coloca cola',posicion
        self.colaIn.put(posicion)
        print "ESTADO DE LA MATRIZ:",self.matriz
    def actualiza(self):
        color_={0:'white',1:'blue',2:'red'}
        self.v0.update()
        while True:
            if not(self.colaOut.empty()):
		
                matrix,status=self.colaOut.get()
                for i in range(len(matrix)):
                     self.nl[i].config(bg=color_[matrix[i]])#color_[i])
                self.matriz[:]=matrix
                if status:
                    print 'RAISING'
                    self.raises(self.declarar_ganador())
            
            self.v0.update()
            
            
class accion_boton:
    def __init__(self,i,f):
        self.i=i
        self.f=f
    def __call__(self):
        return self.f(self.i)
if __name__=='__main__':
    k=kernel(6,5)
    k.trhows()
