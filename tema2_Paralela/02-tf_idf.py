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
        yield '__file_name__', jobconf_from_env('map.input.file')

    def tf_reducer(self, key, values):
        file_names = set()
        if key == '__file_name__':
            for file in values:
                file_names.add(file)
            yield '__total_file_number__', len(file_names)
        else:
            yield key, sum(values)
       
    def idf_mapper(self, key, values):
        if key != '__total_file_number__':
            yield key[0], key[1]

    def idf_reducer(self, key, values):
        #puede no ser eficiente en el uso de la memoria list(values). 
        #Alternativa: recorrer y contar
        yield key, len(list(values))

    def steps(self):
        return [
            MRStep(mapper = self.tf_mapper,
                    reducer = self.tf_reducer),
            MRStep(mapper = self.idf_mapper,
                    reducer = self.idf_reducer) 
        ]

if __name__ == '__main__':
    MRTf_Idf.run()
