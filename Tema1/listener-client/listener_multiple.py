from multiprocessing.connection import Listener

listener = Listener(address=('147.96.80.75', 6000), authkey='secret password')
print 'listener starting'
while True:
    con1 = listener.accept()
    print '1. connection accepted from', listener.last_accepted
    con2 = listener.accept()
    print '2. connection accepted from', listener.last_accepted
    m1 = con1.recv()
    print '1. received message:', m1    
    m2 = con2.recv()
    print '2. received message:', m2
    con1.send(m2)
    con2.send(m1)
    con1.close()
    con2.close()
    print 'connections closed'
listener.close()
