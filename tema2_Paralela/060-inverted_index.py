# -*- coding: utf-8 -*-

from mrjob.job import MRJob
import string 

class MRInvertedIndex(MRJob):

    def mapper(self, _, line):
        for x in string.punctuation:
            line = line.replace(x,' ')
        words = line.split()
        line_number = words[0]
        for word in words[1:]:
            yield (word.lower(), line_number)
       
    def reducer(self, word, lines):
        line_index = []
        for l in lines:
            if not l in line_index:
                line_index.append(l)
        yield word, line_index
       
if __name__ == '__main__':
    MRInvertedIndex.run()
