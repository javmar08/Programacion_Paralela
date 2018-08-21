from multiprocessing import Process
from multiprocessing import Manager
from multiprocessing import Lock

import time
import random

N = 10 # numero filosofos
K = 600 # numero de iteraciones de cada filosofo

def filosofo(num,tenedor1,tenedor2):
    for i in range(K):
        print "Filosofo ",num, "piensa...(",i,")"
        print "Filosofo ",num, "quiere comer...(",i,")"        

        tenedor1.acquire()
        tenedor2.acquire()

        print "Filosofo ",num, "comido...(",i,")"        

        tenedor1.release()
        tenedor2.release()
                   
if __name__ == '__main__':
  
    tenedores = []
    for i in range(N):
        tenedores.append(Lock())
        
    filosofos = []
    for i in range(N-1):
        filosofos.append(Process(target=filosofo, args=(i,tenedores[i],tenedores[i+1])))
    filosofos.append(Process(target=filosofo, args=(N-1,tenedores[0],tenedores[N-1])))    

    for i in range(N):
        filosofos[i].start()
    
        
