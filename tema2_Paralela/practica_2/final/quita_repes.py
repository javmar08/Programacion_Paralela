# -*- coding: utf-8 -*-
"""
Created on Tue May 19 11:53:34 2015

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
        par=[]
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
            pare=[ip,sesion,pagina,codigo]
            par.append(pare)
        for [a,b,c,d] in par:
            yield (ip,b),[a,b,c,d]
    def behevier(self,key,value):
        behevier=[]
        for word in value:
            ip=word[0]
            dia=word[1]
            if (word[3])==str(200):
                behevier.append(word[2])
                #si la queremos ordenar poner behevier.sort()
        behevierf=sinrepes(behevier)
        lista=[ip,dia,behevierf]      
        yield (ip,behevierf), lista
        
    def contadores(self,key,value):
        repes=0
        dias=[]
        for word in value:
            ip=word[0]
            dia=word[1]
            behevier=word[2]
            repes=repes+1
            dias.append(dia)
        sesiones=len(dias)
        lista=[ip,sesiones,behevier,repes]
        yield behevier,lista
        
    def lista_user(self,key,value):
        user=[]
        fin=[]
        ips=[]
        for word in value:
            ip=word[0]
            user.append(ip)
            behevier=word[2]
            sesiones=word[1]
            repes=word[3]
            par=[ip,sesiones,repes]
            ips.append(par)
        for [ip,sesiones,repes] in ips:
            lista=[ip,sesiones,behevier,repes,user]
            fin.append(lista)
        for ele in  fin:
            yield ele[0],ele
            
    def total_sesiones(self,key,value):
        comportamientos=[]
        num_total=0
        for word in value:
            ip=word[0]
            num_total=num_total+word[1]
            behevier=word[2]
            repes=word[3]
            user=word[4]
            compor=[ip,behevier,repes,user]
            comportamientos.append(compor)
        for [a,b,c,d] in comportamientos:
            #en la lista no enviamos la ip
            yield a,[num_total,b,c,d]

    def steps(self):
        return [
            MRStep(mapper = self.mapper,
                   reducer = self.sesiones),
            MRStep(reducer = self.behevier),
            MRStep(reducer = self.contadores),
            MRStep(reducer = self.lista_user),
            MRStep(reducer = self.total_sesiones)
            
            
            
        ]
            
if __name__ == '__main__':
    MRTf_Idf.run()