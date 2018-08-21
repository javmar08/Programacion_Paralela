# -*- coding: utf-8 -*-

from mrjob.job import MRJob
from mrjob.step import MRStep
from mrjob.compat import jobconf_from_env
import sys
import string 

class MRTf(MRJob):

    def mapper(self, _, line):
        for x in string.punctuation:
            line = line.replace(x,' ')
        line = line.split()
        for word in line:
            yield (word.lower(), jobconf_from_env('map.input.file')), 1
        yield '__file_name__', jobconf_from_env('map.input.file')

    def reducer(self, key, values):
        file_names = set()
        if key == '__file_name__':
            for file in values:
                file_names.add(file)
            yield '__total_file_number__', len(file_names)
        else:
            yield key, sum(values)

class MRIdf(MRJob):
    def mapper(self, _, line):
        l = line.split()
        yield l[0], (l[1], l[2], l[3])

    def reducer(self, word, values): 
        docs_in = set()
        results = []
        for d, n, D in values:
            docs_in.add(d)
            results.append(((word,d),(n,D)))
        K = len(docs_in)
        for (word,d),(n,D) in results:
            yield (word,d), (n,K,D)

"""
Implementa la versión básica del tf-idf de es.wikipedia 
Con estos dos pasos hacemos todas las cuentas necesarias, en 
el primer reduce obtenemos el tf(word,doc) y el D (total_file_number)

En el segundo paso obtenemos el número de documentos en los que aparece cada 
palabra.
"""

if __name__ == '__main__':

    print 'Starting tf job'
    job_tf = MRTf(args=sys.argv[1:])
    runner_tf = job_tf.make_runner()
    runner_tf.run()
    tf_output = []
    for line in runner_tf.stream_output():
        tf_output = tf_output + [job_tf.parse_output_line(line)]
    print 'Results tf:', tf_output
    
    D = tf_output[0][1]
    f = open('results_tf.txt','w')
    for [word, doc], n in tf_output[1:]:
        f.write(word+'\t'+doc+'\t'+str(n)+'\t'+str(D)+'\n')
    f.close()

    print 'Starting idf job'
    job_idf  = MRIdf(args=['results_tf.txt'])
    runner_idf = job_idf.make_runner()
    runner_idf.run()
    idf_output = []
    for line in runner_idf.stream_output():
        idf_output = idf_output + [job_idf.parse_output_line(line)]
    print 'Results idf:', idf_output
    
