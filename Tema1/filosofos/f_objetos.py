# -*- coding: utf-8 -*-
from multiprocessing import Lock, Process
import time
import random

##DEADLOCK solution###

class Filosofo:
    K = 600 #número de iteraciones
    def __init__(self, n, tenedores):
        self.num = n
        self.tenedores = tenedores
    def run(self):
        for i in range(Filosofo.K):
            print "Filosofo ",self.num, "piensa...(",i,")"
            print "Filosofo ",self.num, "quiere comer...(",i,")"        

            self.tenedores[self.num].acquire()
            self.tenedores[(self.num+1)%N].acquire()

            print "Filosofo ",self.num, "comido...(",i,")"

            self.tenedores[self.num].release()
            self.tenedores[(self.num+1)%N].release()

               
    
if __name__ == '__main__':
    N = 5 #número de filosofos
    tenedores = [Lock() for count in range(N)]    
    for i in range(N):
        p = Process(target=Filosofo(i,tenedores).run, args=()) 
        p.start()

        
