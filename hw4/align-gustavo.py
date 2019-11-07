#!/usr/bin/env python
import optparse, sys, os, logging
from collections import defaultdict
from itertools import islice

optparser = optparse.OptionParser()
optparser.add_option("-d", "--datadir", dest="datadir", default="data", help="data directory (default=data)")
optparser.add_option("-p", "--prefix", dest="fileprefix", default="hansards", help="prefix of parallel data files (default=hansards)")
optparser.add_option("-e", "--english", dest="english", default="en", help="suffix of English (target language) filename (default=en)")
optparser.add_option("-f", "--french", dest="french", default="fr", help="suffix of French (source language) filename (default=fr)")
optparser.add_option("-l", "--logfile", dest="logfile", default=None, help="filename for logging output")
optparser.add_option("-t", "--threshold", dest="threshold", default=0.5, type="float", help="threshold for alignment (default=0.5)")
optparser.add_option("-n", "--num_sentences", dest="num_sents", default=sys.maxsize, type="int", help="Number of sentences to use for training and alignment")
(opts, _) = optparser.parse_args()
f_data = "%s.%s" % (os.path.join(opts.datadir, opts.fileprefix), opts.french)
e_data = "%s.%s" % (os.path.join(opts.datadir, opts.fileprefix), opts.english)

if opts.logfile:
    logging.basicConfig(filename=opts.logfile, filemode='w', level=logging.INFO)

bitext = [[sentence.strip().split() for sentence in pair] for pair in islice(zip(open(f_data), open(e_data)), opts.num_sents)]
f_count = defaultdict(int)
e_count = defaultdict(int)
fe_count = defaultdict(int)

# initialize t0 - Easy choice: initialize uniformly
probs = defaultdict()
probs[0] = defaultdict()

for french,english in bitext:
    for f in french:
        for e in english:
            probs[0][(f,e)] = 1 / len(french)

k = 0
num_iterations = 5
converged = False

while converged == False:
    k += 1
    
    # initialize all counts to zero
    f_count = defaultdict(int)
    e_count = defaultdict(int)
    fe_count = defaultdict(int)
    probs[k] = defaultdict(int)
    
    # sys.stdout.write('-> Initiating counts')
    for (n, (f, e)) in enumerate(bitext):
        for f_i in set(f):
            f_count[f_i] += 1
            for e_j in set(e):
                fe_count[(f_i,e_j)] += 1
        for e_j in set(e):
            e_count[e_j] += 1
    
    for (n, (f, e)) in enumerate(bitext):
        for f_i in set(f):
            Z = 0 ## Z commonly denotes a normalization term
            
            for e_j in set(e):
                probs[k-1][(f_i,e_j)] = fe_count[(f_i,e_j)] / e_count[e_j]
                Z += probs[k-1][(f_i,e_j)]
                
            for e_j in set(e):
                c = probs[k-1][(f_i,e_j)]/Z
                fe_count[(f_i,e_j)] += c
                e_count[e_j] += c
                
    for (fek, (f_i, e_j)) in enumerate(fe_count.keys()):
        probs[k][(f_i,e_j)] = fe_count[(f_i,e_j)] / e_count[e_j]

    if k >= num_iterations: converged = True

probabilities = probs[k]
alignment_words = defaultdict(int)
alignment_pos = defaultdict(int)

for (n, (f, e)) in enumerate(bitext):
    for (i, f_i) in enumerate(set(f)):
        bestp = 0
        beste = None
        bestj = 0
        for (j, e_j) in enumerate(set(e)):
            if probabilities[(f_i,e_j)] > bestp:
                bestp = probabilities[(f_i,e_j)]
                bestj = j
                beste = e_j
        alignment_words[f_i] = beste
        alignment_pos[i] = bestj

for (f, e) in bitext:
  for (i, f_i) in enumerate(set(f)): 
    sys.stdout.write("%i-%i " % (i,alignment_pos[i]))
  sys.stdout.write("\n")