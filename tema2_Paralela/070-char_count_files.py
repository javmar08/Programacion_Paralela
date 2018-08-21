# -*- coding: utf-8 -*-

from mrjob.job import MRJob
from mrjob.compat import jobconf_from_env
from mrjob.step import MRStep

import string 

class MRCharCount(MRJob):

    def mapper(self, _, line):
        yield jobconf_from_env('map.input.file'), len(line)
                    
    def reducer(self, file, chars):
        yield None, (file, sum(chars))
        
    def total(self, _, values):
        file_list = []
        total = 0
        for (file, chars) in values:
            file_list.append((file,chars))
            total += chars
        for (file, chars) in file_list:
            yield file, (chars, total)

    def steps(self):
        return [
            MRStep(mapper = self.mapper,
                   reducer = self.reducer),
            MRStep(reducer = self.total) 
        ]
  
if __name__ == '__main__':
    MRCharCount.run()
