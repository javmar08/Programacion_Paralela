# -*- coding: utf-8 -*-

from mrjob.job import MRJob
import string

class MRWordAppearances(MRJob):
   
    def mapper(self, _, line):
        for x in string.punctuation:
            line = line.replace(x,' ')
        for word in line.split():
            yield (word.lower(), 1)

    def reducer(self, word, counts):
        n = sum(counts)
        self.increment_counter('group', 'total_words', n)
        yield n, word

if __name__ == '__main__':
    print 'Starting map-reduce job'
    job = MRWordAppearances(args=['060-lines.txt'])
    runner = job.make_runner()
    runner.run()
    tmp_output = []
    for line in runner.stream_output():
        tmp_output = tmp_output + [job.parse_output_line(line)]
    tmp_output.sort()
    print 'Results:', tmp_output
    print runner.counters()

