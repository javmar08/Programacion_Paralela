from mrjob.job import MRJob
from mrjob.step import MRStep
import string 

class MRWordAppearances(MRJob):
    SORT_VALUES = True

    def mapper(self, _, line):
        for x in string.punctuation:
            line = line.replace(x,' ')
        words = line.split()
        for word in words:
            yield (word.lower(), 1)
        yield '.total_counter.', len(words) 

    def reducer(self, word, counts):
        yield None, (word, sum(counts))
    
    def frequency(self, _, data):
        first_value = data.next()
        assert first_value[0] == '.total_counter.'
        total = first_value[1]
        for word, counts in data: 
            yield word, counts/float(total)
    
    def steps(self):
        return [
            MRStep(mapper = self.mapper,
                    reducer = self.reducer),
            MRStep(reducer = self.frequency) 
        ]

if __name__ == '__main__':
    MRWordAppearances.run()
