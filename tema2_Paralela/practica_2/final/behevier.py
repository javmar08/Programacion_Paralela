# -*- coding: utf-8 -*-
"""
Created on Thu May 21 10:51:49 2015

@author: alumno
"""

from mrjob.job import MRJob
from mrjob.step import MRStep
from mrjob.compat import jobconf_from_env
import string 
import time 
from time import strptime
pattern="%d/%b/%Y:%H:%M:%S"

#funciones auxiliares para quitar repetidos de una lista
def esta(x,lista):
    aux=False
    if len(lista)==0:
        aux=False
    else:
        for i in range(len(lista)):
            if lista[i]==x:
                aux=True
    return aux
    
def sinrepes(lista):
    solu=[]
    for ele in lista:
        if esta(ele,solu):
            pass
        else:
            solu.append(ele)
    return solu
    
#clase para hacer el mapper reducer
class MRTf_Idf(MRJob):
    def mapper(self, _, line):
        #ponemos el if para evitar erroes con lineas vacias
        if line !="":
            words=line.split()
            ip=words[0]
            #par=fecha,pagina,accion
            fecha=time.mktime(strptime(words[3][1:],pattern))
            #dia=words[3][1:12]
            par=[ip,fecha,words[6],words[8]]
            yield ip,par
        else:
            pass
        
    def sesiones(self,key,value):
        tiempo=3600
        actual=[]
        sesion=1
        for word in value:
            if len(actual)==1:
                if word[1]<(actual[0]+tiempo):
                    actual.remove(actual[0])
                    actual.append(word[1])
                else:
                    actual.remove(actual[0])
                    actual.append(word[1])
                    sesion=sesion+1
            else:
                actual.append(word[1])
            ip=word[0]
            pagina=word[2]
            codigo=word[3]
            yield (ip,sesion), [pagina,codigo]
            
    def behevier(self,key,value):
        behevier=[]
        for word in value:
            ip=key[0]
            if (word[1])==str(200):
                behevier.append(word[0])
        behevierf=sinrepes(behevier)
        yield ip, behevierf
        
    def steps(self):
        return [
        MRStep(mapper = self.mapper,
                reducer = self.sesiones),
                MRStep(reducer = self.behevier)
            
        ]
            
if __name__ == '__main__':
    MRTf_Idf.run()