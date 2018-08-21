# -*- coding: utf-8 -*-
"""
Created on Tue Apr  7 12:24:33 2015

@author: alumno
"""

from multiprocessing.connection import Listener
from multiprocessing import Process
from multiprocessing import AuthenticationError
from time import time

def recibidor(conn,id):

#    print 'connection accepted from', listener.last_accepted
    quit = True
    while quit:
        try:
            m = conn.recv()
        except 'EDFError':
            print 'connection ha petao abruptly'
            break
        print 'reciviendo mensaje',m,'from', id
        if m == 'hola':
            conn.send('adios'+str(time()))
        else:
            conn.send('wtf')
    print 'connection closed'
    conn.close()
    
listener = Listener(address=('147.96.18.211',6000), authkey='secret password')

while True:
    print 'accepting connecions'
    try:
        conn = listener.accept()
        print 'connection acepted from', listener.last_accepted
        proceso = Process(target=recibidor, args=(conn,listener.last_accepted))
        proceso.start()
    except AuthenticationError:
        print 'conection refused'

listener.close()
    