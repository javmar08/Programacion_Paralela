# -*- coding: utf-8 -*-
"""
Created on Tue Apr 28 12:23:50 2015

@author: alumno
"""

from mrjob.job import MRJob

#esto es un filtro con MRJob pero quitando el condicion if del ejemplo anterior
class MRCharCount(MRJob):
    
    def mapper(self,_,line):
        yield ('map' in line.lower()),1      
    #filtramos buscando la palabra map, pero evitando el if
    #la funcion lower lo que hace es pasar todo a minusculas
      
            
    def reducer(self,key,values):
        yield key, sum(values)
        
if __name__=='__main__':
    MRCharCount.run()
    
#para ejecutar en termina poner python clasemrjob.py nombre de fichero del que hay que leer
