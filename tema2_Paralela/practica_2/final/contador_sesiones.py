# -*- coding: utf-8 -*-
"""
Created on Thu May 21 11:00:53 2015

@author: alumno
"""
from mrjob.job import MRJob
import time 
from time import strptime
pattern="%d/%b/%Y:%H:%M:%S"


class MRTf_Idf(MRJob):
    
    def mapper(self, _, line):
        #ponemos el if para evitar erroes con lineas vacias
        if line !="":
            words=line.split()
            ip=words[0]
            fecha=time.mktime(strptime(words[3][1:],pattern))  
            yield ip,fecha
        else:
            pass
    def reducer(self,key,value):
        tiempo=3600
        actual=[]
        sesion=1
        for word in value:
            if len(actual)==1:
                if word<(actual[0]+tiempo):
                    actual.remove(actual[0])
                    actual.append(word)
                else:
                    actual.remove(actual[0])
                    actual.append(word)
                    sesion=sesion+1
            else:
                actual.append(word)
        yield key,sesion
        
if __name__ == '__main__':
    MRTf_Idf.run()