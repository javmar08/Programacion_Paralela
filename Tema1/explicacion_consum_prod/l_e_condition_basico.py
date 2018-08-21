# -*- coding: utf-8 -*-
from multiprocessing import Process
from multiprocessing import Condition
from multiprocessing import Manager
import time, random

K = 3;


'''
los trapicheos se hacen a la hora de entrar y de salir.
una vez dentro, las condiciones del while se encargan de dejar
entrar a los que están fuera
'''
def lector(c,nu): # además hay uqe pasar el tablero, y la posicion, conn
    # Este for no hay que ponerlo
    for x in range(K):
        # pide entrar
        c.acquire()
        # si el número de escritores es mayor que 0, esperas
        while (nu[0] > 0): # condicion (nu[0] > 0 or nu[1] > 0):
            print "lector espera............."
            c.wait()
           
        #cuando has salido, sumamos uno a los escritores
           # que esrán dentro
        nu[1] = nu[1] + 1
        c.release()
        
        # esta es la parte de escribir en el tablero
        # aquí editas la lista del tablero            
        print "Lector lee de la DB", x, "Estado: escritores", nu[0], "lectores", nu[1] 
        '''
            if tablero[posicion]== 8:
                tablero[posicion]=0
                conn.send(0)
            else:
                conn.send(1) 1 equivale a que está ocupado
        '''
        # esto no hace falta
        time.sleep(random.random())
        
        c.acquire()
        nu[1] = nu[1] - 1
        
        # notify_all
        if nu[1] == 0:
            c.notify_all()
        c.release()
        
        print "Tablero editado con exito"
        print "Lector piensa en lo que ha leido", x

def escritor(c,nu):   # copias y pegas cambiando 
    for x in range(K):
        print "Escritor piensa lo que va a escribir", x

        c.acquire()
        while (nu[0] > 0 or nu[1] > 0):
            print "escritor espera................."
            c.wait()
        nu[0] = nu[0] + 1
        c.release()
            
        print "Escritor escribe en la DB", x, "Estado: escritores", nu[0], "lectores", nu[1] 
        time.sleep(random.random())

        c.acquire()
        nu[0] = nu[0] - 1
        c.notify_all()
        c.release()

if __name__ == '__main__':
    NL = 5 #numero lectores
    NE = 2 #numero escritores

    manager = Manager()
    nu = manager.list([0,0]) #numero de usuarios, nu[0] escritores, nu[1] lectores.
    # nu numero de jugadores que están escribiendo en el tablero
    # en nuestro caso puede ser 0,0 , 0,1 o 1,0
    c = Condition()
    '''
    si quieres un contdor de jugadores
    
    num_jugadores = manager.list([0,0])
    '''
    
    l = []
    for x in range(NL):
        l.append(Process(target=lector, args=(c, nu)))
    e = []
    for x in range(NE):        
        e.append(Process(target=escritor, args=(c, nu)))

    for x in e+l:
        x.start()
    for x in e+l:
        x.join()
