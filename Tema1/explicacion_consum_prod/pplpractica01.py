# -*- coding: utf-8 -*-
"""
Created on Tue Apr 14 11:19:32 2015

@author: alumno
"""

from multiprocessing.connection import Listener
from random import randint
from multiprocessing import Process
from multiprocessing import Manager
from multiprocessing import Condition

def jugador0(conexion,ultima_conexion,tablero,control,jugando,equipo):
    control.acquire()
    while(jugando[0]==True or jugando[1]==True):
        control.wait()
        print 'esperando'
    jugando[0]=jugando[0]+1
    control.release()
    #aqui todo lo de modificar el tablero
    mensaje=conexion.recv()
    num_filas=0
    num_colum=18
    editar_ok=editar_tablero(mensaje,tablero)
    carta=(editar_ok, (num_filas, num_colum, [tablero]))
    #termina
    control.acquire()
    jugando[0]=jugando[0]-1
    if jugando[0]==False:
        control.notify_all()
    control.release()
    print 'tablero editado'
    return carta
        

def jugador1(conexion,ultima_conexion,tablero,control,jugando,equipo):   
    control.acquire() 
    while(jugando[0]==True or jugando[1]==True):
        control.wait()
        print 'esperando'
    jugando[1] = jugando[1]+1
    control.release()
    #aqui va todo lo de modificar el tablero
    mensaje=conexion.recv()
    num_filas=0
    num_colum=18
    editar_ok=editar_tablero(mensaje,tablero)
    carta=(editar_ok, (num_filas, num_colum, [tablero]))
    #termina
    control.acquire()
    jugando[1]=jugando[1]-1
    if jugando[1]==False:
        control.notify_all()
    control.release()
    print 'tablero editado'
    return carta
def jugar(conexion,ultima_conexion,tablero,control,jugando,equipo):
    while not estaLleno(tablero):
        if equipo==0:
            enviar=jugador0(conexion,ultima_conexion,tablero,control,jugando,equipo)
        else:
            enviar=jugador1(conexion,ultima_conexion,tablero,control,jugando,equipo)
        conexion.send(enviar)
    if estaLleno(tablero):
        conexion.send(3)
            
#funciones auxiliares

def estaLleno(tablero):
    auxiliar=True
    for i in range (len(tablero)):
        if tablero[i]==8:
            auxiliar=False
    return auxiliar

def editar_tablero(mensaje, tablero):
    output = 1
    print 'están intentando editar el tablero'
    try:
        posicion=mensaje[1]
        equipo=mensaje[0]
        if tablero[posicion] == 8:
            #un mensaje es una tupa (equipo, posicion)
            tablero[posicion] = equipo
            output =0 
    except:
        pass
    return output            
            
    
if __name__== "__main__":
    
    print 'esperando conexion'
#    listener= Listener(address=('147.96.18.215', 6000),authkey='secret')
    listener= Listener(address=('localhost', 6000),authkey='secret')

    manager=Manager()
    tablero=manager.list([8]*16)
    control = Condition()
    jugando=manager.list([0,0])
    while True:
        conexion= listener.accept()
    
        print 'Se ha conectado', listener.last_accepted
        equipo=randint(0,1)
        conexion.send(equipo)
        p= Process(target=jugar,args=(conexion,listener.last_accepted,tablero,control,jugando,equipo))
        p.start()
#        p.join()
    listener.close()
    
    
"""
def editar_tablero(mensaje, tablero, last_accepted):
    output = 'Fail' # esto ahora es un 1
    print listener.last_accepted, 'está intentando editar el tablero'
    try:
        if tablero[mensaje[1]] == 'Empty':
#            un mensaje es una tupa (equipo, posicion)
            tablero[mensaje[1]] = mensaje[0]
            output = 'Ok' // esto ahora es un cero
    except:
        pass
    return output
    

editar_ok = editar_tablero(.....)
conn.send(editar_ok, (num_filas, num_colum, [tablero]))
"""

