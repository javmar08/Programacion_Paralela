# -*- coding: utf-8 -*-
"""
Created on Thu Apr 16 18:54:52 2015

@author: javier

Comentarios sobre la practica:
El servidor se divide en tres partes:

La primera formada por las funciones jugador0 jugador1 y jugar que son las que utilizamos para hacer la concurrencia del tablero,
donde se envian los mensajes al cliente. Las funciones jugador0 y jugador1 son iguales cambiando algunos 0 por 1. La funcion jugador
se basa en el uso de condicionales con la condicion del while de que si hay alguien jugando, es decir la variable jugando[0] o jugando[1] son 1, es decir,
hay alguien jugando o que no se el turno de tu equipo y haya jugadores del otro equipo en espera los demas procesos pasan a esperar y mientras el jugador que esta jugando pasa a editar el tablero.
La funcion jugar se basa en un bucle que mientras en tablero no este lleno ejecuta las funciones jugador1 o jugador0 dependiendo
del equipo al que pertenece el proceso. Una vez que se llena el tablero entra en un if que dice que ya se ha acabado y hace un 
recuento del numero de ceros y unos para saber quien ha gando y envia el mensaje

La segunda parte de la practica son las funciones auxiliares editar_tablero que edita el tablero pero lo que manda es una contestacion
de si se ha editado o no el tablero, para luego enviarsela posteriormente al cliente. Tambien esta las funciones estaLleno que mira
recorriendo la lista si el tablero esta lleno o no, y las funciones numero0 y numeros1 que nos dice el numero de ceros y de unos que hay
en el tablero para luego poder diferenciar al ganador

La tercera parte de la practica es el main donde definimos el manager, el condition, el tablero, jugando, el listener y con un bucle while True
vamos aceptando conexiones y arrancando cada conexion como si fuese un proceso asigandolas un valor 0 o 1 correspondiente al equipo que
van a ir mediante un randit(0,1).

el tablero hace referencia a una matriz 4X4 de la siguiente forma, los cuatro primeros numeros serian la fila 1, los cuatro siguientes la fila2
los cuatro siguientes la fila 3 y los cuatro ulitmos la fila 4.

NOTA:CONTROL DE ACCESO AL TABLERO
Para acceder al tablero es necesario saber que usaremos tres variables que son listas manejadas por un manager. La lista jugando que puede
tener los siguientes valores [0,0] [1,0] [0,1] indica si hay algun jugador editando el tablero que se señala con un uno e indica de que equipo es
dependiendo de si la posicion del uno en la lista es la 0 o 1. Luego esta la variable turno que tambien es una lista manejada por el manager que
toma valores 0 y 1 para indicar si el turno es para jugadores del equipo 0 o 1. Por ultimo esta la lista de espera que que en la posicion 0 
de la lista tiene en el numero de jugadores del equipo 0 que hay esperando para jugar y en la poscicion 1 tiene el numero de jugadores del 
equipo 1 esperando a jugar.

La condicion para poder editar el tablero es que no haya nadie editando el tablero es decir que jugando valga [0,0], que sea nuestro turno
o que no haya nadie jugando, no sea nuestro turno pero no haya nadie esperando del equipo al que le toca jugar lo que les saltaria el turno
Lo principal para que no entren varios jugadores a la vez en el tablero es la condicion de que no haya nadie editando el tablero para poder pasar,7
luego con esa condicion sola podiamos limitar que solo entre uno cada vez al tablero, pero para que no haya inanicion y que un proceso entre siemrpre
por ser mas rapido se pone el turno asi evitamos que si un jugador1 puede siempre entrar antes que un jugador del equipo 0, pero esto puede dar problemas
de deadlock ya que si no hay jugadores del otro equipo por el turno se quedaria el prograba en un stanby por lo que añadimos la lista espera que nos 
hace ver si hay alguien en espera y al ver que no hay nadie en espera del equipo al que le toca jugar se les salta el turno evitando el deadlock.
"""

from multiprocessing.connection import Listener
from random import randint
from multiprocessing import Process
from multiprocessing import Manager
from multiprocessing import Condition

#Primera parte: las funciones para jugar y hacer la concurrencia del tablero

def jugador0(conexion,ultima_conexion,tablero,control,jugando,espera,equipo,turno):   
    
    if True:
        control.acquire()
        while ((jugando[0]==True or jugando[1]==True) or (turno[0]==1 and espera[1]>0)):
            print 'esperando'
            conexion.send('en estado de espera')
            espera[0] =espera[0] + 1
            control.wait()
            espera[0] = espera[0] - 1
        
        jugando[0]=jugando[0]+1
        control.release()
        #aqui todo lo de modificar el tablero
        mensaje=conexion.recv()
        if int(mensaje[1][1])==5:
            conexion.send('desconectar')
        else:
            editar_ok=editar_tablero(mensaje,tablero)
            conexion.send(editar_ok)
        #termina
        control.acquire()
        turno[0]=1
        jugando[0]=jugando[0]-1
        control.notify_all()
        control.release()
    
        print 'tablero editado'
        

def jugador1(conexion,ultima_conexion,tablero,control,jugando,espera,equipo,turno):
    if True:
        control.acquire() 
        while ((jugando[0]==True or jugando[1]==True) or (turno[0]==0 and espera[0]>0)):
            print 'esperando'
            conexion.send('en estado de espera')
            espera[1] = espera[1] + 1
            control.wait()
            espera[1] = espera[1] - 1
        
        jugando[1] = jugando[1]+1
        control.release()
        #aqui va todo lo de modificar el tablero
        mensaje=conexion.recv()
        if int(mensaje[1][1])==5:
            conexion.send('desconectar')
        else:
            editar_ok=editar_tablero(mensaje,tablero)
            conexion.send(editar_ok)
        #termina
        control.acquire()
        turno[0]=0
        jugando[1]=jugando[1]-1
        control.notify_all()
        control.release()
    
        print 'tablero editado'
    
def jugar(conexion,ultima_conexion,tablero,control,jugando,espera,equipo,turno):
    while not estaLleno(tablero):
        conexion.send(str(tablero))
        if equipo==0:
            jugador0(conexion,ultima_conexion,tablero,control,jugando,espera,equipo,turno)
        else:
            jugador1(conexion,ultima_conexion,tablero,control,jugando,espera,equipo,turno)
            
    if estaLleno(tablero):
        #conexion.send('fin de la partida, pulsar otra vez a enviar para saber quien ha ganado')
        if numero1(tablero)<numero0(tablero):
            conexion.send('GAME OVER: GANA EQUIPO 0')
        elif numero0(tablero)<numero1(tablero):
            conexion.send('GAME OVER: GANA EQUIPO 1')
        else:
            conexion.send('GAME OVER: EMPATE')
            
            
#Segunda parte:funciones auxiliares

def estaLleno(tablero):
    auxiliar=True
    for i in range (len(tablero)):
        if tablero[i]==8:
            auxiliar=False
    return auxiliar

def editar_tablero(mensaje, tablero):
    print 'están intentando editar el tablero'
    posicion=(mensaje[1])
    try:
        output = 'esa posicion ya estaba cogida'
        #posicion=mensaje[1]
        equipo=mensaje[0]
        fila=int(posicion[1])
        columna=int(posicion[3])
        if fila==0:
            if int(tablero[columna]) == 8:
                #un mensaje es una tupa (equipo, posicion)
                tablero[columna] = equipo
                output ='movimiento realizado'
        
        elif fila==1:
            if int(tablero[columna+4]) == 8:
                #un mensaje es una tupa (equipo, posicion)
                tablero[columna+4] = equipo
                output ='movimiento realizado'
                
        elif fila==2:
            if int(tablero[columna+8]) == 8:
                #un mensaje es una tupa (equipo, posicion)
                tablero[columna+8] = equipo
                output ='movimiento realizado'
                
        elif fila==3:
            if int(tablero[columna+12]) == 8:
                #un mensaje es una tupa (equipo, posicion)
                tablero[columna+12] = equipo
                output ='movimiento realizado'
    except:
        pass
    return output   
    
#detallitos para mejorar y saber luego quien gana
def numero1(tablero):
    con=0
    i=0
    while i<len(tablero):
        if tablero[i]==1:
            con=con+1
        i=i+1
    return con
def numero0(tablero):
    con=0
    i=0
    while i<len(tablero):
        if tablero[i]==0:
            con=con+1
        i=i+1 
    return con

#Tercera parte el main           
if __name__== "__main__":
        
    print 'esperando conexion'
    listener= Listener(address=('localhost', 6000),authkey='secret')

    manager=Manager()
    tablero=manager.list([8]*16)
    jugando=manager.list([0,0])
    espera=manager.list([0,0])
    control = Condition()
    turno=manager.list([randint(0,1)])
    jugador=0
    
    while True:
        conexion= listener.accept()
    
        print 'Se ha conectado', listener.last_accepted
        jugador=jugador+1
        equipo=jugador%2
        #equipo=randint(0,1)
        conexion.send(equipo)
        p= Process(target=jugar,args=(conexion,listener.last_accepted,tablero,control,jugando,espera,equipo,turno))
        p.start()
    listener.close()
    
    


    




