from multiprocessing.connection import Listener

listener = Listener(address=('147.96.80.75', 6000), authkey='secret password')

print 'listener starting'

conn = listener.accept()
print 'connection accepted from', listener.last_accepted

while True:
    m = conn.recv()
    print 'received message:', m
    if m == "hola":
        conn.send("response: adios")
    else:
        conn.send("response: ?")
conn.close()
print 'connection closed'
listener.close()
