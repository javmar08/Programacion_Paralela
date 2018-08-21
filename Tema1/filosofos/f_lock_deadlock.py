from multiprocessing import Process
from multiprocessing import Lock

import time
import random

N = 5 # numero filosofos
K = 600 # numero de iteraciones de cada filosofo

def filosofo(num,tenedores):
    for i in range(K):
        print "Filosofo ",num, "piensa...(",i,")"
        print "Filosofo ",num, "quiere comer...(",i,")"        

        tenedores[num].acquire()
        tenedores[(num+1)%N].acquire()

        print "Filosofo ",num, "comido...(",i,")"        

        tenedores[num].release()
        tenedores[(num+1)%N].release()
                   
if __name__ == '__main__':
  
    tenedores = []
    for i in range(N):
        tenedores.append(Lock())
        
    filosofos = []
    for i in range(N):
        filosofos.append(Process(target=filosofo, args=(i,tenedores)))

    for i in range(N):
        filosofos[i].start()
    
        
