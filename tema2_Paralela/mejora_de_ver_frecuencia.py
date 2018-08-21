# -*- coding: utf-8 -*-
"""
Created on Thu Apr 30 11:41:10 2015

@author: alumno
"""

from mrjob.job import MRJob
from mrjob.step import MRStep
import string


class MRCharCount(MRJob):
    #es para que las claves las ordene por valor
    SORT_VALUES=True
    
    def mapper(self,_,line):
        #sustituimos los signos de puntuacion por espacios en blanco
        for x in string.punctuation:
            line.replace(x,' ')
        #para contarlas cada palabra tiene que hacer de llave
        words=line.split()
        for x in (line.split()):
            yield (x.lower(),1) 
        yield '.total_counter.', len(words)
        
    def sum_words(self,x,counts):
            yield None,(x,sum(counts))
            
    def reducer(self,_,data):
        first_value=data.next()
        assert first_value[0]=='.total_counter.'
        total=first_value[1]
        for (palabra,valor) in data:
            yield palabra,valor/float(total)
        
    #cuando ponemos mas funciones que mapper y reducer lo que hacemos es crear un steps para indicar el orden en el que van los
    #procesos        
    def steps(self):
        return [MRStep(mapper=self.mapper,reducer=self.sum_words),MRStep(reducer=self.reducer)]
            
if __name__=='__main__':
    MRCharCount.run()
    
