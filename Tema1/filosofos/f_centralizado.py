from multiprocessing import Process
from multiprocessing import Condition
from multiprocessing import Manager

import time
import random

N = 5 # numero filosofos
K = 10 # numero de iteraciones de cada filosofo

def filosofo(num,camarero,tenedores):
    for i in range(K):
        print "Filosofo ",num, "piensa...(",i,")"  
        time.sleep(random.random()/4)
        print "Filosofo ",num, "quiere comer...(",i,")"        
        print tenedores
        
        camarero.acquire()
        while not(tenedores[num] and tenedores[(num+1)%N]):
            print "Filosofo ",num, "espera..."      
            camarero.wait()        
        tenedores[num] = False
        tenedores[(num+1)%N] = False
        print tenedores
        camarero.release()

        print "Filosofo ",num, "come...(",i,")"
        time.sleep(random.random()/3)
        print "Filosofo ",num, "termina de comer.(",i,")" 

        camarero.acquire()
        tenedores[num] = True
        tenedores[(num+1)%N] = True
        camarero.notify_all()
        camarero.release()
                   
if __name__ == '__main__':
    
    camarero = Condition()
    manager = Manager()
    tenedores = manager.list()

    for i in range(N):
        tenedores.append(True)
    
    filosofos = []
    for i in range(N):
        filosofos.append(Process(target=filosofo, args=(i,camarero,tenedores)))
    for i in range(N):
        filosofos[i].start()
    for i in range(N):
        filosofos[i].join()
    
        
