# -*- coding: utf-8 -*-
"""
Created on Thu Apr 30 10:15:36 2015

@author: alumno

Ver que palabra aparece mas veces
"""

from mrjob.job import MRJob
from mrjob.step import MRStep
import string


class MRCharCount(MRJob):
    
    def mapper(self,_,line):
        #sustituimos los signos de puntuacion por espacios en blanco
        for x in string.punctuation:
            line.replace(x,' ')
        #para contarlas cada palabra tiene que hacer de llave
        for x in (line.split()):
            yield (x.lower(),1)    
    def sum_words(self,x,counts):
            yield None,(sum(counts),x)
            
    def reducer(self,_,values):
        maxi=0
        max_word=''
        for (counts,x) in values:
            if counts>maxi:
                maxi=counts
                max_word=x
        yield max_word,maxi
        
    #cuando ponemos mas funciones que mapper y reducer lo que hacemos es crear un steps para indicar el orden en el que van los
    #procesos        
    def steps(self):
        return [MRStep(mapper=self.mapper,reducer=self.sum_words),MRStep(reducer=self.reducer)]
            
if __name__=='__main__':
    MRCharCount.run()
    

#para ejecutar en termina poner python clasemrjob.py nombre de fichero del que hay que leer