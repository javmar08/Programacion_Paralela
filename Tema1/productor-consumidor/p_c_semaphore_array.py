from multiprocessing import Process
from multiprocessing import BoundedSemaphore
from multiprocessing import current_process
from multiprocessing import Array
from multiprocessing import Value

import time
import random

#el amacen ya tiene capacidad K, lo que podemos almacernar varios datos sin ser consumidos

N = 20
K = 5

def delay(factor = 5):
    time.sleep(random.random()/factor)

def p(almacen,indice,poner,tomar):
    for v in range(N):
        print current_process().name, "produciendo",
        delay()
        poner.acquire()
        almacen[indice.value] = v
        delay()
        indice.value = indice.value + 1
        print current_process().name, "almacenando", v
        tomar.release()

def c(almacen,indice,poner,tomar):
    for v in range(N):
        tomar.acquire()        
        print current_process().name, "desalmacenando",
        dato = almacen[0]
        indice.value = indice.value - 1
        delay()
        for i in range(indice.value):
            almacen[i] = almacen[i + 1]
        poner.release()
        print current_process().name, "consumiendo", dato
        delay()
        
if __name__ == "__main__":

    poner = BoundedSemaphore(K) 
    tomar = BoundedSemaphore(K)
    for i in range(K):
        tomar.acquire()

    almacen = Array('i', K)
    indice = Value('i',0)

    print "almacen inicial", almacen[:], "indice", indice.value

    productor = Process(target=p, name="productor", args=(almacen,indice,poner,tomar))
    consumidor = Process(target=c, name="consumidor", args=(almacen,indice,poner,tomar))

    productor.start()
    consumidor.start()
   
