# -*- coding: utf-8 -*-

from mrjob.job import MRJob
from mrjob.compat import jobconf_from_env
from mrjob.step import MRStep
import string 

class MRCharCount(MRJob):

    def mapper(self, _, line):
        n = len(line)
        self.increment_counter('group', 'total_chars', n)
        yield jobconf_from_env('map.input.file'), n
                    

    def reducer(self, file, chars):
        yield file, sum(chars)
        
  
if __name__ == '__main__':
    MRCharCount.run()
