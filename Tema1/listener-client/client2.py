from multiprocessing.connection import Client

print 'trying to connect'
conn = Client(address=('147.96.80.75', 6000), authkey='secret password')
print 'sending message'
conn.send("holaa")
print 'received message', conn.recv() 
conn.close()
