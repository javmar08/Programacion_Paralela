# -*- coding: utf-8 -*-
"""
Created on Tue Apr 28 12:16:08 2015

@author: alumno
"""

from mrjob.job import MRJob

#esto es un filtro con MRJob
class MRCharCount(MRJob):
    
    def mapper(self,_,line):
        #filtramos buscando la palabra map
        if 'map' in line:
            yield 'si', 1 #line pones line en vez de 1 si queremos que nos muestre un str de la linea que contiene la palabra, 1 si queremos contar cuantas veces aparece
        else:
            yield 'no', 1 #line
            
    def reducer(self,key,values):
        yield key, sum(values)
        
if __name__=='__main__':
    MRCharCount.run()
    
#para ejecutar en termina poner python clasemrjob.py nombre de fichero del que hay que leer
