from multiprocessing import Process
from multiprocessing import Condition
from multiprocessing import current_process
from multiprocessing import Manager

N = 5000
K = 3

def p(almacen,control,i): 
    for v in range(N):
        print current_process().name, "produciendo"
        control.acquire()
        while len(almacen) == K:
            print current_process().name, "esperando..."
            control.wait()
        dato = str(i)+"."+str(v)+"+"		
        almacen.append(dato)
        print current_process().name, "almacenando", dato
        control.notify_all()
        control.release()                 

def c(almacen,control):
     for v in range(N):
        control.acquire()        
        while len(almacen) == 0:
            print current_process().name, "esperando.."
            control.wait()
        print current_process().name, "desalmacenando"
        dato = almacen.pop(0)
        control.notify_all()
        control.release()
        print current_process().name, "consumiendo", dato[:-1]+"-"  
        
if __name__ == "__main__":

    control = Condition()
    manager = Manager()
    l = manager.list()
    print "almacen inicial", l[:]

    productor = Process(target=p, name="productor1", args=(l,control,1))
    productor2 = Process(target=p, name="productor2", args=(l,control,2))
    consumidor = Process(target=c, name="consumidor", args=(l,control))
    consumidor2 = Process(target=c, name="consumidor2", args=(l,control))
    
    productor.start()
    productor2.start()

    consumidor.start()
    consumidor2.start()

    productor.join()
    productor2.join()
    consumidor.join()
    consumidor2.join()
