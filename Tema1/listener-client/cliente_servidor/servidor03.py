
# -*- coding: utf-8 -*-
#aqui se conecta a un servidor por eso no podemos respondernos


from multiprocessing.connection import Listener
from multiprocessing import Process
from multiprocessing import AuthenticationError
from time import time

def recibidor(conn):

#    print 'connection accepted from', listener.last_accepted
    quit = True
    while quit:
        try:
            m = conn.recv()
        except:
            print 'connection ha petao abruptly'
            break
        if m == 'quit':
            quit = False
        print 'received message : ', m
        conn.send('esta respuseta se genera automaticamente')
#        conn.close()
#        print 'connection closed'
    print 'connection closed'
    conn.close()
    
listener = Listener(address=('147.96.18.211',6000), authkey='secret password')

while True:
    print 'accepting connecions'
    try:
        conn = listener.accept()
        print 'connection acepted from', listener.last_accepted
        proceso = Process(target=recibidor, args=(conn,))
        proceso.start()
    except AuthenticationError:
        print 'conection refused'

listener.close()