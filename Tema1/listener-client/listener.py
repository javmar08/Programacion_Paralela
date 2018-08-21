# -*- coding: utf-8 -*-
"""
Created on Thu Mar 26 10:31:45 2015

@author: javier

el programa lo que hace es que cada vez que el canal esta creado en conn=listener
y la conexion se ha establecido yo decido hacer cosas con esa conexion, cuando yo
recibo estoy esperando a que me mande un mensaje m,estoy esperando el numero de cliente con una 
"""

from multiprocessing.connection import Listener

listener=Listener(address=('147.96.18.200',6000),authkey='secret password')

print 'listener starting'
cont=0
while True:
    conn=listener.accept()
    print 'conectin accepted from', listener.last_accepted
    m=conn.recv()
    print 'recived message:',m
    if m=='hola':
        conn.send('client number'+str(cont)+"adios")
    else:
        conn.send('cliente number'+str(cont)+'?')
    conn.close()
    cont=cont+1
    print 'conection closed'
listener.close()