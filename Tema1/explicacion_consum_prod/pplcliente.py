# -*- coding: utf-8 -*-
"""
Created on Tue Apr 14 11:31:40 2015

@author: alumno
"""

from multiprocessing.connection import Client

print 'trying to connect'
conn = Client(address=('192.168.190.171',6000),authkey='secret password')
hemosTerminado=False
while not hemosTerminado:
    movimiento=raw_input("introduce un movimiento: ")
    conn.send(movimiento)
    while True:
            answer = conn.recv()
            print 'recibido'
    
conn.close()