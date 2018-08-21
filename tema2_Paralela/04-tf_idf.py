# -*- coding: utf-8 -*-
"""

Una vez que se calcula el D en el primer reducer,
seguir la misma idea que en  047 para poder pasar ese
valor a todos los demás
El primer map
w,d,1 'counter',d
El reduce
_,(w,d,n) y _ ,(!,D)
ordenación secundaria,
usamos el primer !,D y luego
emitimos (w,d) n,D
...

"""
from mrjob.job import MRJob
from mrjob.step import MRStep
from mrjob.compat import jobconf_from_env

import string 

class MRTf_Idf(MRJob):
    SORT_VALUES = True
    
    def tf_mapper(self, _, line):
        for x in string.punctuation:
            line = line.replace(x,' ')
        line = line.split()
        for word in line:
            yield (word.lower(), jobconf_from_env('map.input.file')), 1
        yield ('__doc_counter__',None), jobconf_from_env('map.input.file')

    def tf_reducer(self, (word,doc), values):
        if word == '__doc_counter__':
            file_names = set() 
            for file in values:
                file_names.add(file)
            yield None, ('.__total_file_number__.', None, len(file_names))
        else:
            yield None, (word, doc, sum(values))
 
    def agregate(self, _, values):
        word, doc, n = values.next()
        assert word == '.__total_file_number__.'
        D = n
        for word, doc, n in values:
            yield word, (doc,n,D)
       
    def idf_reducer(self, word, values):
        docs_in = set()
        results = []
        for (doc,n,D) in values:
            results.append((doc, n, D))
            docs_in.add(doc)
        K = len(docs_in)
        for (doc,n,D) in results:
            yield (word, doc), (n, K, D)
        
    def steps(self):
        return [
            MRStep(mapper = self.tf_mapper,
                   reducer = self.tf_reducer),
            MRStep(reducer = self.agregate),
            MRStep(reducer = self.idf_reducer) 
        ]

if __name__ == '__main__':
    MRTf_Idf.run()
