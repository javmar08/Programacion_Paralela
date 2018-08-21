# -*- coding: utf-8 -*-

from mrjob.job import MRJob

class MRCharCount(MRJob):
    def mapper(self, _, line):
        self.increment_counter('group', 'total_chars', len(line))
        yield "chars", len(line)  
               
    def reducer(self, key, values):
        yield key, sum(values)

if __name__ == '__main__':
    print 'Starting map-reduce job'
    job = MRCharCount(args=['El_buscón-Quevedo.txt'])
    runner = job.make_runner()
    runner.run()
    tmp_output = []
    for line in runner.stream_output():
        print "****parser", job.parse_output_line(line)
        tmp_output = tmp_output + [line]
    print 'Results:', tmp_output
    print runner.counters()

