# -*- coding: utf-8 -*-
"""
Created on Tue Apr 28 11:29:13 2015

@author: alumno
ejemplo de que el multiprocessing se queda pequño para usar
programacion paralela
"""

from multiprocessing import Pool
from time import time

def f(n):
    sum=0
    for i in xrange(n*n):
        sum+=i
    return sum
    
def g(n):
    sum=0
    for i in xrange(n*n*n):
        sum=sum+(i**3)
    return sum
    
k=500
#el pool divide el trabajo entre 4 trabajadores para que se haga mas rapido y eficiente
pool=Pool(4)

print 'regular map'
init_time=time()
map(g,range(k))
print time()-init_time

print 'paralela map'
init_time=time()
pool.map(g,range(k))
print time()-init_time