# -*- coding: utf-8 -*-
"""
Created on Tue Apr 28 12:28:37 2015

@author: alumno
string.punctuation nos da los signos de puntuacion
con line.replace(for x in string.punctuation,' ') remplaza cada signo de puntuacion por un espacio en blanco
"""

from mrjob.job import MRJob
import string

#esto es un filtro con MRJob pero quitando el condicion if del ejemplo anterior
class MRCharCount(MRJob):
    
    def mapper(self,_,line):
        #sustituimos los signos de puntuacion por espacios en blanco
        for x in string.punctuation:
            line.replace(x,' ')
        #para contarlas cada palabra tiene que hacer de llave
        for x in (line.split()):
            yield x,1
            
    def reducer(self,key,values):
        #hay que usar variables auxiliares pq solo vale la primera vez que lo hace, por eso guardamos mejor los valores en variables auxiliares
        #para ver la diferencia en lo explicado arriba cambiar n por sum(values) y observar
        n=sum(values)
        if n==2:
            yield key, n
        
if __name__=='__main__':
    MRCharCount.run()
    
#para ejecutar en termina poner python clasemrjob.py nombre de fichero del que hay que leer
