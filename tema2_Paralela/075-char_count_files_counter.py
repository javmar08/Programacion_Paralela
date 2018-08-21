# -*- coding: utf-8 -*-

from mrjob.job import MRJob
from mrjob.compat import jobconf_from_env
from mrjob.step import MRStep

import string 

class MRCharCount(MRJob):

    def mapper(self, _, line):
        yield jobconf_from_env('map.input.file'), len(line)
                    

    def reducer(self, file, chars):
        n = sum(chars)
        self.increment_counter('group', 'total_chars', n)
        yield file, n
        
  
if __name__ == '__main__':
    MRCharCount.run()
