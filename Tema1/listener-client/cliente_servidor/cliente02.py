# -*- coding: utf-8 -*-

from multiprocessing.connection import Client


print 'trying to conect'
conn = Client(address=('147.96.18.204', 6000), authkey = 'secret password')
while True:
    mess = raw_input('¿Qué quieres que envíe?')
    print 'sending message'
    conn.send(mess)
    print 'Respuesta :', conn.recv()
conn.close()