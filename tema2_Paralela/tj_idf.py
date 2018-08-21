# -*- coding: utf-8 -*-
"""
Created on Thu May  7 10:32:22 2015

@author: alumno
"""

from mrjob.job import MRJob
from mrjob.step import MRStep
from mrjob.compat import jobconf_from_env
import string 

class tj_idf(MRJob):
    def mapper(self, _, line):
        for x in string.punctuation:
            line = line.replace(x,' ')
        words = line.split()
        lista=[]
        for word in words:
            lista.append(word.lower())
        for x in lista:
            yield x,jobconf_from_env('map.input.file') #el jobconf_from_env... te dice el fichero en el que estas trabajando
            
    def reducer(self, key, counts):
        num=0
        lista=[]
        for fichero in counts:
            num=num+1
        lista.append([key,num,fichero])
        final=[]
        for (key,num,fichero) in lista:
            for j in range(len(final)):
                if key == lista[j][0]:
                    lista[j][1]=lista[j][1]+num
                    lista[j][2]=lista[j][2]+fichero
                else:
                    final.append([key,num,fichero])
    
        for z in range(len(final)):
            yield final[z][0],[final[z][1],final[z][0]] 
            
            

if __name__ == '__main__':
    tj_idf.run()

    