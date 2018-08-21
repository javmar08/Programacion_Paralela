from multiprocessing import Process
from multiprocessing import Condition
from multiprocessing import current_process
from multiprocessing import Manager

N = 5000
K = 1

def p(almacen,control): 
    for v in range(N):
        print current_process().name, "produciendo"
        control.acquire()
        while len(almacen) == K:
            print current_process().name, "esperando..."
            control.wait()
        almacen.append(v)		
        print current_process().name, "almacenando", v
        control.notify()
        control.release()                 

def c(almacen,control):
     for v in range(N):
        control.acquire()        
        while len(almacen) == 0:
            print current_process().name, "esperando.."
            control.wait()
        print current_process().name, "desalmacenando"
        dato = almacen.pop(0)
        control.notify()
        control.release()
        print current_process().name, "consumiendo", dato  
        
if __name__ == "__main__":

    control = Condition()
    manager = Manager()
    l = manager.list()
    print "almacen inicial", l[:]

    productor = Process(target=p, name="productor", args=(l,control))
    consumidor = Process(target=c, name="consumidor", args=(l,control))

    productor2 = Process(target=p, name="productor2", args=(l,control))
    consumidor2 = Process(target=c, name="consumidor2", args=(l,control))


    
    productor.start()
    consumidor.start()
    productor2.start()
    consumidor2.start()
    productor.join()
    consumidor.join()
    productor2.join()
    consumidor2.join()
