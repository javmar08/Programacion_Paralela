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

"creamos el servidor"
def recibidor(conexion,cliente,tablero,control,turno,equipo):
    conexion.send(str(tablero))
    while not estaLleno(tablero):
        conexion.send(str(tablero))
        (m,n)=conexion.recv()
        posicion=pasar(n)
        if m == 'quit':
            break
        else:
            "mejorar el juego"
            while turno == 0:
                control.acquire()
                if equipo==0:
                    if esVacia(tablero,posicion):
                        tablero=jugar(tablero,posicion)
                        control.wait()
                        turno = 1
                        conexion.send('ficha colocada')
                    else:
                        control.wait()
                        conexion.send('ahi ya hay una ficha puesta')
                        turno=1
                        
                else:
                    conexion.send('no es tu turno')
                    control.wait()
                control.notify_all()
                control.release()
            while turno==1:
                control.acquire()
                if equipo==1:
                    if esVacia(posicion,tablero):
                        tablero=jugar(tablero,posicion)
                        control.wait()
                        turno=0
                        conexion.send('ficha colocada')
                    else:
                        control.wait()
                        conexion.send('ahi ya hay una ficha puesta')
                        turno=0
                else:
                    conexion.send('no es tu turno')
                    control.wait()
                control.notify_all()
                control.release()
    if estaLleno(tablero):
        print 'FIN'
        if numero1(tablero)<numero0(tablero):
            print 'gana el equipo 0'
            conexion.send('gana el equipo 0')
        else:
            print 'gana el equipo 1'
            conexion.send('gana el equipo 1')
                
    conexion.close()

"funciones auxiliares"
def pasar(n):
    return int(n)
    
def estaLleno(tablero):
    auxiliar=True
    for i in range (len(tablero)):
        if tablero[i]==8:
            auxiliar=False
    return auxiliar

def esVacia(posicion,tablero):
    auxiliar=False
    if tablero[posicion]==8:
        auxiliar=True
    return auxiliar
            
def numero1(tablero):
    con=0
    i=0
    while i<len(tablero):
        if tablero[i]==1:
            con=con+1
        i=i+1
def numero0(tablero):
    con=0
    i=0
    while i<len(tablero):
        if tablero[i]==0:
            con=con+1
        i=i+1
def jugar(tablero,posicion,equipo):
    i=posicion
    if tablero[i]==8:
        tablero[i]=equipo
    return tablero
    
    
if __name__== "__main__":
    
    print 'esperando conexion'
#    listener= Listener(address=('147.96.18.215', 6000),authkey='secret')
    listener= Listener(address=('localhost', 6000),authkey='secret')

    manager=Manager()
    tablero=manager.list([8]*16)
    control = Condition()
    turno=randint(0,1)
    while True:
        conexion= listener.accept()
    
        print 'Se ha conectado', listener.last_accepted
        equipo=randint(0,1)
        conexion.send(equipo)
        p= Process(target=recibidor,args=(conexion,listener.last_accepted,tablero,control,turno,equipo))
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

