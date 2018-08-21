from multiprocessing import Process
from multiprocessing import Manager
from multiprocessing import Lock

import time
import random

N = 5 # numero filosofos
K = 200 # numero de iteraciones de cada filosofo

def filosofo(num,tenedores):
    for i in range(K):
        print "Filosofo ",num, "piensa...(",i,")"
        print "Filosofo ",num, "quiere comer...(",i,")"        

        while True:
                tenedores[num].acquire()
                print "Filosofo ",num, "consigue tenedor", num
                if tenedores[(num+1)%N].acquire(False):
                    break
                else:
                    tenedores[num].release()
                    print "Filosofo ",num, "libera tenedor", num

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
    
        
