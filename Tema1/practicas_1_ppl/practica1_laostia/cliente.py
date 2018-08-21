# -*- coding: utf-8 -*-
'''
El protocolo implementado es prácticamente la acordada en clase.
Por un lado esta el servidor (en el archivo server.py) definido en 
la clase kernel que lanza los siguientes procesos (en self.throws)
-carga_nuevos_jugadores: esta a la espera de nuevos jugadores (conexiones)
         a las que envia el mensaje 
         (int self.color,(int dim_i,int dim_j))
         donde (int dim_i,int dim_j) son las coordenadas del tablero
         y color \in {0,1} es el equipo
         La nueva conexion se transpasa a un proceso (funcion kernel.check)
         que gestiona la comunicacion con ese cliente
-kernel.check<=>player: la conexion en el player se abstrae un poco, es el
        metodo mover(k) el que se encarga de enviar el mensaje del movimiento
        efectuado (int k) y devuelve lo recibido:
        
                    (int code,(int din_i,int dim,_j),[int] tablero)
        
        donde el code es:
        
    -code==0:No es tu turno, por lo que no se colocó nada
    -code==1: Era tu turno y hemos colocado tu movimiento.
    -code==2:Era tu turno pero el moviento es invalido. envia otro mensaje cuando 
             cuando la penalización de tiempo acabe (con el mismo mensaje por lo que 
             además no se le da más información).

-player<=>interface: Al estar estos dos programas siempre en el mismo ordenador se
    puede simplificar usando un par de Queue(s) una para cada dirección de la los 
    mensajes
    -player=>interface en la cola (colaTableros) se añaden  ([int] tableros,int status) e interfaz los actualiza en un 
           proceso (ver método interface.actualiza), el status\in{0,1} indica si se ha terminado el juego (1) o no (0)
    -interface=>player:en la cola (colaJugadas)se añade los int movimientos que el player envia (player.juega,player.mueve)


Justicia:
    La justicia implementada es bastante simple, si es el turno del jugador mueve y pasa ser el turno del otro
    Si por contra es el turno del adversario, y hay adversarios esperando se pierde el movimiento y se pasa al 
    siguiente. Pero si no hay adversarios esperando el jugador efectuará su jugada y el turno permanecera en el
    adversario.
        Independientemente de como se consiga jugar, si el jugador mueve algo inválido se le castiga sin poder 
    mover durante 1 segundo.
'''

from multiprocessing.connection import Client
from multiprocessing import Process,Queue
print 'trying to connect'
print 'send a message'
from time import sleep
from random import shuffle
from servidor import interface
lista_mov=[]
class player:
    def __init__(self,colaJugadas,colaTableros):
        self.con=Client(address=('localhost',6000),authkey='secret password')
        
        (self.color,(self.dim_i,self.dim_j))=self.con.recv()
        self.tablero=[0]*(self.dim_i*self.dim_j)        
        self.lista_mov=[]
        self.colaJugadas=colaJugadas#cola de jugadas desde el intefaz
        self.colaTableros=colaTableros#cola de Tableros provenientes hacia el interfaz
        for i in range(self.dim_i*self.dim_j):
                self.lista_mov.append(i)
    def mover(self,k):
        print 'muev'
        self.con.send((self.color,(k)))
        print 'mover env'
        a=self.con.recv()
        if a[0]==2:#espera
            a=self.con.recv()
        return a
    def gana(self):
        adversario=1-self.color
        R=len(filter(lambda x: x==self.color,self.tablero))-len(filter(lambda x: x==adversario,self.tablero))
        return R
    def termina(self):
        self.con.send('q')
        #self.colaTableros.put((self.tablero[:],1))
    def juega(self):
        print 'a'
        jugadas=(self.lista_mov[:])
        shuffle(jugadas)
        cont=0
        #el protocolo dice que un juego termina con el comando 3
        while cont!=3:            
            m=self.colaJugadas.get()
            print 'm',m
            
            print m
            (cont,_,_,self.tablero)=self.mover(m)
            print 'cont',cont
            self.colaTableros.put((self.tablero[:],0))
            sleep(1.0)
        self.colaTableros.put((self.tablero[:],1))
        self.termina()   
        
if __name__=='__main__':
    
    ju=[]
    H=[]
    colaJugadas,colaTableros=Queue(),Queue()
    P=player(colaJugadas,colaTableros)
    Interfaz=interface(P.color,P.dim_i,P.dim_j,colaJugadas,colaTableros)
    
    P.interfaz=Interfaz
    ju.append(Process(target=P.juega))
    H.append(Process(target=Interfaz.actualiza))
    for (i,j) in zip(ju,H):
        i.start()
        j.start()
        print 'another player'
