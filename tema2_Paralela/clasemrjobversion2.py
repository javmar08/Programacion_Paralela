# -*- coding: utf-8 -*-
"""
Created on Tue Apr 28 12:04:25 2015

@author: alumno
"""

from mrjob.job import MRJob

#lo que hace es contar los caracteres de un fichero que le pasemos
class MRCharCount(MRJob):
    
    def mapper(self,_,line):
        #la funcion del mapper es clasificar cada elemento por la clave que se le da juntandolas y ordenandolas
        yield 'chars', len(line)
        #el split lo que hace es quitar los espacios en blanco
        yield 'words', len(line.split())
        yield 'lines', 1
        #el maper lo que hace es devolver un par con una clava (chater) y el numero de caracteres que hay en esa linea
        
    def reducer(self,key,values):
        #devolvemos un par con el key, que da informacion sobre lo que devolvemos y el value, que devuelve el valor
        #en este caso key dara chars y value la cantidad de caracteres por linea
        #el reducer lo que hace es que para cada key ejucuta la suma de los que tienen la misma key
        yield key,sum(values)
        
if __name__=='__main__':
    MRCharCount.run()
    
#para ejecutar en termina poner python clasemrjob.py nombre de fichero del que hay que leer
