from multiprocessing import Process
from multiprocessing import BoundedSemaphore
from multiprocessing import current_process
from multiprocessing import Array
from multiprocessing import Value
from multiprocessing import Lock

import time
import random
N = 20
K = 5

def delay(factor = 3):
    time.sleep(random.random()/factor)

#el almacen tiene capacidad K

def p(almacen,indice,poner,tomar,almacenar):
    for v in range(N):
        print current_process().name, "produciendo",
        poner.acquire()
        almacenar.acquire()
        almacen[indice.value] = v    
        delay()
        indice.value = indice.value + 1
        almacenar.release()
        print current_process().name, "almacenando", v
        tomar.release()

def c(almacen,indice,poner,tomar,almacenar):
    for v in range(N):
        tomar.acquire()        
        print current_process().name, "desalmacenando",
        almacenar.acquire()
        dato = almacen[0]
        indice.value = indice.value - 1
        delay()
        for i in range(indice.value):
            almacen[i] = almacen[i + 1]
        almacenar.release()
        poner.release()
        print current_process().name, "consumiendo", dato

        
if __name__ == "__main__":

    poner = BoundedSemaphore(K)  
    tomar = BoundedSemaphore(K)
    for i in range(K):
        tomar.acquire()

    almacenar = Lock()

    almacen = Array('i', K)
    indice = Value('i',0)

    print "almacen inicial", almacen[:], "indice", indice.value

    productor = Process(target=p, name="productor", args=(almacen,indice,poner,tomar,almacenar))
    consumidor = Process(target=c, name="consumidor", args=(almacen,indice,poner,tomar,almacenar))

    productor.start()
    consumidor.start()

