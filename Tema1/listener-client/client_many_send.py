from multiprocessing.connection import Client
from time import sleep

print 'trying to connect'
conn = Client(address=('147.96.80.75', 6000), authkey='secret password')

print 'sending messages'
conn.send("hola")
sleep(1)
conn.send("como te va?")
conn.send("adios")
while True:
    print 'received message', conn.recv() 
conn.close()
