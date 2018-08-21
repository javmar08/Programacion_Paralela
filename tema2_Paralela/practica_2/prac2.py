# -*- coding: utf-8 -*-
"""
Created on Mon May 18 00:05:13 2015

@author: javier
"""

# -*- coding: utf-8 -*-
"""
Created on Thu May 14 10:16:39 2015

@author: alumno
"""
from mrjob.job import MRJob
from mrjob.step import MRStep
from mrjob.compat import jobconf_from_env
import string 
import time 
from time import strptime
pattern="%d/%b/%Y:%H:%M:%S"

class MRTf_Idf(MRJob):

    def mapper(self, _, line):
        words=line.split()
        ip=words[0]
        #par=fecha,pagina,accion
        #fecha=time.mktime(strptime(words[3][1:],pattern))
        dia=words[3][1:12]
        par=[ip,dia,words[6],words[8]]
        yield (ip,dia),par
        
    def behevier(self,key,value):
        behevier=[]
        for word in value:
            ip=word[0]
            dia=word[1]
            if int(word[3])==200:
                behevier.append(word[2])
        lista=[ip,dia,behevier]      
        yield (ip,behevier), lista
        
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
            yield a,[a,num_total,b,c,d]

    def steps(self):
        return [
            MRStep(mapper = self.mapper,
                   reducer = self.behevier),
            MRStep(reducer = self.contadores),
            MRStep(reducer = self.lista_user),
            MRStep(reducer = self.total_sesiones)
            
            
            
        ]
if __name__ == '__main__':
    MRTf_Idf.run()
