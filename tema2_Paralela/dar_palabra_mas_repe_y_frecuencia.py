# -*- coding: utf-8 -*-
"""
Created on Thu Apr 30 10:53:43 2015

@author: alumno
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
        total=0
        lista=[]
        for (counts,x) in values:
            total=total+counts
            lista.append((x,counts))
        for (palabra,valor) in lista:
            yield palabra,[valor,str((float(valor)/total)*100)+' %']
        
    #cuando ponemos mas funciones que mapper y reducer lo que hacemos es crear un steps para indicar el orden en el que van los
    #procesos        
    def steps(self):
        return [MRStep(mapper=self.mapper,reducer=self.sum_words),MRStep(reducer=self.reducer)]
            
if __name__=='__main__':
    MRCharCount.run()
    
