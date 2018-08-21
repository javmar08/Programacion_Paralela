# -*- coding: utf-8 -*-
"""
Created on Thu Mar 26 10:17:02 2015

@author: javier

La definicion en conn es para conectar con alguien a traves de una direccion IP
que es addrees y authkey es la contraseña del servidor mediante el comando Client
El client siempre lleva la ip de la persona a la que se quiere conectar
Con el for lo que hacemos es enviar varios mensajes, sin el for solo mandaria uno
"""

from multiprocessing.connection import Client

print "trying to connect"
conn=Client(address=('147.96.18.202',6000),authkey='secret password')
for i in range(3):
    message=raw_input('dame un mensaje: ')
    print 'ENVIANDO MENSAJE'
    conn.send(str(message))
    print 'recibiendo mensaje', conn.recv()
    
conn.close()