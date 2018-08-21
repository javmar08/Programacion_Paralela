# -*- coding: utf-8 -*-

from mrjob.job import MRJob
from mrjob.step import MRStep
from mrjob.compat import jobconf_from_env

import string 

class MRTf_Idf(MRJob):

    def tf_mapper(self, _, line):
        for x in string.punctuation:
            line = line.replace(x,' ')
        line = line.split()
        for word in line:
            yield (word.lower(), jobconf_from_env('map.input.file')), 1

    def tf_reducer(self, (word,doc), values):
        yield word, (doc, sum(values))
       
    def idf_reducer(self, word, values):
        docs_in = set()
        doc_freq = []
        for (doc, freq) in values:
            doc_freq.append((doc,freq))
            docs_in.add(doc)
        K = len(docs_in)
        for (doc, freq) in doc_freq:
            yield (word, doc), (freq, K)
        
    def steps(self):
        return [
            MRStep(mapper = self.tf_mapper,
                    reducer = self.tf_reducer),
            MRStep(reducer = self.idf_reducer) 
        ]

if __name__ == '__main__':
    MRTf_Idf.run()
