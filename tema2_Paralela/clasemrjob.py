# -*- coding: utf-8 -*-
"""
Created on Tue Apr 28 11:41:21 2015

@author: alumno
vamos a usar el paquete mrjob para usar mapReduce

range(10) genera la lista y la guarda en memoria
xrange(10) no crea la lista, sino un generador que te da la informacion cuando la necesitas
la unica ventaje es que es mas eficiente
"""

from mrjob.job import MRJob

#lo que hace es contar los caracteres de un fichero que le pasemos
class MRCharCount(MRJob):
    
    def mapper(self,_,line):
        yield 'chars', len(line)
        #el maper lo que hace es devolver un par con una clava (chater) y el numero de caracteres que hay en esa linea
        
    def reducer(self,key,values):
        #devolvemos un par con el key, que da informacion sobre lo que devolvemos y el value, que devuelve el valor
        #en este caso key dara chars y value la cantidad de caracteres por linea
        #el reducer lo que hace es que para cada key ejucuta la suma de los que tiene la misma key
        yield key,sum(values)
        
if __name__=='__main__':
    MRCharCount.run()
    
#para ejecutar en termina poner python clasemrjob.py nombre de fichero del que hay que leer
