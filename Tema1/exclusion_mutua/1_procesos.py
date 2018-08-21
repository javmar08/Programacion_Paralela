# -*- coding: utf-8 -*-

import time
import random

from multiprocessing import Process

def f(value):
    for i in range(3):
        print "hola soy", value, "vuelta", str(i)
        time.sleep(random.random()/3)

def g():
    print "adios"


if __name__ == "__main__":
    N = 30
    lp = []
    for i in range(N):
        lp.append(Process(target=f,args=("ana "+str(i),)))
    for p in lp:
        p.start()

    q = Process(target=g)
    q.start()
    print "fin"
    
