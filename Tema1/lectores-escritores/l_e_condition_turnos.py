from multiprocessing import Process
from multiprocessing import Condition
from multiprocessing import Manager
import time, random

K = 5;

def lector(c, nu, ne, turno):
    for x in range(K):

        c.acquire()
        while (nu[0] > 0 or (turno[0] == 0 and ne[0] > 0 ) ):
            print "lector espera............."
            ne[1] = ne[1] + 1            
            c.wait()
            ne[1] = ne[1] - 1            
                        
        nu[1] = nu[1] + 1
        c.release()
                    
        print "Lector lee de la DB", x, "Estado: escritores", nu[0], "lectores", nu[1] 
        time.sleep(random.random())
        
        c.acquire()
        turno[0] = 0
        nu[1] = nu[1] - 1
        if nu[1] == 0:
            c.notify_all()
        c.release()

        print "Lector piensa en lo que ha leido", x

def escritor(c, nu, ne, turno):    
    for x in range(K):
        print "Escritor piensa lo que va a escribir", x

        c.acquire()
        while (nu[0] > 0 or nu[1] > 0 or (turno[0] == 1 and ne[1] > 0)):
            print "escritor espera................."
            ne[0] = ne[0] + 1
            c.wait()
            ne[0] = ne[0] - 1

        nu[0] = nu[0] + 1
        c.release()
            
        print "Escritor escribe en la DB", x, "Estado: escritores", nu[0], "lectores", nu[1], "turno", turno[0] 
        time.sleep(random.random())

        c.acquire()
        turno[0] = 1       
        nu[0] = nu[0] - 1
        c.notify_all()
        c.release()

if __name__ == '__main__':
    #Resolver inanicion de los escritores: si escritor espera los lectores
    # no pueden pasar
    NL = 5
    NE = 2

    manager = Manager()
    nu = manager.list([0,0]) #numero de usuarios de la base de datos
    ne = manager.list([0,0]) #numero de usuarios en espera: 0 escritores, 1 lectores
    turno = manager.list([0]) #turno: valor 0 para escritores, valor 1 para lectores

    c = Condition()

    l = []
    for x in range(NL):
        l.append(Process(target=lector, args=(c, nu, ne, turno)))
    e = []
    for x in range(NE):        
        e.append(Process(target=escritor, args=(c, nu, ne, turno)))

    for x in e+l:
        x.start()
    for x in e+l:
        x.join()
