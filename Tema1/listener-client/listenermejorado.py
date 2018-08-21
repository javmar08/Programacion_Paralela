0# -*- coding: utf-8 -*-
"""
Created on Thu Mar 26 11:09:33 2015

@author: alumno

el listener siempre tiene la ip de la maquina y el client tiene la ip de la persona
a la que te quieres conectar
"""

from multiprocessing.connection import Listener

listener=Listener(address=('147.96.18.200',6000),authkey='secret password')

print 'listener starting'
conn=listener.accept()
print 'conectin accepted from', listener.last_accepted
#a diferncia del otro listener aqui el listener.accept va fuera pq solo hay que hacertar una vez
#la conexion y luego recibir con el while todos los mensajes del Client
while True:
    m=conn.recv()
    print 'recived message:',m
    if m=='hola':
        conn.send('response: adios')
    else:
        message=raw_input('contesta al mensaje: ')
        conn.send(message)
conn.close()
print 'conection closed'
listener.close()