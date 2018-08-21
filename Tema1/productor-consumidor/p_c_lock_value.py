from multiprocessing import Process
from multiprocessing import Lock
from multiprocessing import current_process
from multiprocessing import Value
from time import sleep
from random import random

N = 10

def p(almacen, lock):
    for v in range(N):
        print current_process().name, "produciendo",
        sleep(random()/3)
        lock.acquire()
        almacen.value = v    
        lock.release()
        print current_process().name, "almacenando", v
       

def c(almacen, lock):
    for v in range(N):
        lock.acquire()
        print current_process().name, "desalmacenando",       
        dato = almacen.value
        lock.release()
        print current_process().name, "consumiendo", dato
        sleep(random()/3)
         
if __name__ == "__main__":

    almacen = Value('i', -1)
    print "almacen inicial", almacen.value

    lock = Lock()

    productor = Process(target=p, name="productor", args=(almacen, lock))
    consumidor = Process(target=c, name="consumidor", args=(almacen, lock))

    consumidor.start()
    productor.start()
    
   
