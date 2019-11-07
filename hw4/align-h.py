#!/usr/bin/env python
import optparse, sys, os, logging
from collections import defaultdict
from itertools import islice
import math


# train the word alignment model
def train_alignment(bitext, iterations=1):
    # Probabilities of word translation pairs
    probs = defaultdict(defaultdict)
    probs[0] = initialize_probs(bitext)

    # Add null words into each source sentence
    # add_null_words(bitext, probs[0])

    f_vocab = list(set([word_f for [sent_f, sent_e] in bitext for word_f in sent_f]))

    for k in range(1, iterations+1):
        # Expected counts
        count = defaultdict(float)
        count_e = defaultdict(float)

        # Update counts
        for (sent_f, sent_e) in bitext:
            for w_f in sent_f:
                Z = 0

                for w_e in sent_e:
                    Z += probs[k-1][(w_f, w_e)]

                for w_e in sent_e:
                    c = probs[k-1][(w_f, w_e)]/Z
                    count[(w_f, w_e)] = count[(w_f, w_e)] + c
                    count_e[w_e] = count_e[w_e] + c

        # Update probabilities
        probs[k] = defaultdict()
        for (w_f, w_e) in count:
            # Smoothed probability
            probs[k][(w_f, w_e)] = (count[(w_f, w_e)]+0.005)/(count_e[w_e] + len(f_vocab)*0.005)

        # Stop upon convergence
        if thereis_convergence():
            break

    return probs[iterations]


# TODO: tells if the update is converging
def thereis_convergence():
    return False


# Initialize the probabilities of word translation pairs uniformly. (Baseline initialization)
def _initialize_probs(bitext):
    probs = defaultdict(float)
    f_vocab = list(set([word_f for [sent_f, sent_e] in bitext for word_f in sent_f]))
    e_vocab = list(set([word_e for [sent_f, sent_e] in bitext for word_e in sent_e]))

    for w_f in f_vocab:
        for w_e in e_vocab:
            probs[(w_f, w_e)] = 1/len(f_vocab)

    return probs


# Similar to baseline initialization but only words that co-occur in translation pairs are given above zero
# probabilities. Using this, training is faster and better than the baseline.
def initialize_probs(bitext):
    probs = defaultdict(float)
    sum_by_word = defaultdict(int)

    for sent_f, sent_e in bitext:
        for w_f in sent_f:
            for w_e in sent_e:
                probs[(w_f, w_e)] += 1
                sum_by_word[w_e] += 1

    max_sum = sum_by_word[max(sum_by_word, key=sum_by_word.get)]

    for p in probs:
        probs[p] = probs[p]/max_sum

    return probs


# Initialize the probabilities of word translation pairs with LLR scores
def _initialize_probs(bitext):
    probs = defaultdict(float)
    f_vocab = list(set([word_f for [sent_f, sent_e] in bitext for word_f in sent_f]))
    e_vocab = list(set([word_e for [sent_f, sent_e] in bitext for word_e in sent_e]))

    # Indices of translation pairs where each word occurs
    occurrences = get_occurrences(bitext)

    # Keep track of source word with the largest LLR sum
    llr_sums = defaultdict(float)

    # Get LLR score for each target word
    for w_e in e_vocab:
        for w_f in f_vocab:
            probs[(w_f, w_e)] = llr_score(w_f, w_e, bitext, occurrences)
            llr_sums[w_e] += probs[(w_f, w_e)]

    # Normalize by largest sum
    max_llr_sum = llr_sums[max(llr_sums, key=llr_sums.get)]

    for p in probs:
        probs[p] = probs[p]/max_llr_sum

    return probs


# Returns an LLR score
def llr_score(trans, source, bitext, occurrences):
    trans_s = occurrences[trans]
    source_s = occurrences[source]

    # counts of co-occurrence or non-co-occurrence of translation and source words in a translation pair
    c_yy = len([s for s in source_s if s in trans_s])
    c_ny = len([s for s in source_s if s not in trans_s])
    c_yn = len([s for s in trans_s if s not in source_s])
    c_nn = len(bitext) - c_yy - c_ny - c_yn

    # Avoid math domain error
    if c_yy == 0:
        c_yy += 1
    if c_ny == 0:
        c_ny += 1
    if c_yn == 0:
        c_yn += 1
    if c_nn == 0:
        c_nn += 1

    # Probabilities of absence/presence combinations
    condprob_yy = c_yy/(c_yy + c_ny)
    condprob_ny = c_ny/(c_ny + c_yy)
    condprob_yn = c_yn/(c_nn + c_yn)
    condprob_nn = c_nn/(c_nn + c_yn)

    # Probabilities of translation absence/presence
    prob_trans_y = (c_yy + c_ny)/(c_yy + c_ny + c_yn + c_nn)
    prob_trans_n = (c_yn + c_nn)/(c_yy + c_ny + c_yn + c_nn)

    # Log probabilities
    log_p_yy = max(math.log(condprob_yy) - math.log(prob_trans_y), 0)
    log_p_ny = max(math.log(condprob_ny) - math.log(prob_trans_y), 0)
    log_p_yn = max(math.log(condprob_yn) - math.log(prob_trans_n), 0)
    log_p_nn = max(math.log(condprob_nn) - math.log(prob_trans_n), 0)

    return (c_yy*log_p_yy + c_ny*log_p_ny + c_yn*log_p_yn + c_nn*log_p_nn)**1.3


# Helper method for llr_score(). Get a dictionary of word:list of indices of sentences where word occurs
def get_occurrences(bitext):
    occurrences = defaultdict(list)

    for (i, (sent_f, sent_e)) in enumerate(bitext):
        for w_f in sent_f:
            if i not in occurrences[w_f]:
                occurrences[w_f].append(i)
        for w_e in sent_e:
            if i not in occurrences[w_e]:
                occurrences[w_e].append(i)

    return occurrences


# Add a null word in every source sentence
def add_null_words(bitext, probs):
    all_words_f = len([w for pair in bitext for w in pair[0]])

    for pair in bitext:
        pair[1].append('<Null>')

        for w_f in pair[0]:
            # Multiplied by a constant to simulate multiple null words per sentence
            probs[(w_f, '<Null>')] += 7/all_words_f


# Get word alignments
def get_alignment(probabilities, bitext):
    alignment_pos = []

    for (sent_f, sent_e) in bitext:
        sent = defaultdict()

        for (i, w_f) in enumerate(sent_f):
            best_p = 0
            best_j = 0

            for (j, w_e) in enumerate(sent_e):
                if probabilities[(w_f, w_e)] > best_p:
                    best_p = probabilities[(w_f, w_e)]
                    best_j = j

            sent[i] = best_j

        alignment_pos.append(sent)

    return alignment_pos


if __name__ == '__main__':
    optparser = optparse.OptionParser()
    optparser.add_option("-d", "--datadir", dest="datadir", default="data", help="data directory (default=data)")
    optparser.add_option("-p", "--prefix", dest="fileprefix", default="hansards",
                         help="prefix of parallel data files (default=hansards)")
    optparser.add_option("-e", "--english", dest="english", default="en",
                         help="suffix of English (target language) filename (default=en)")
    optparser.add_option("-f", "--french", dest="french", default="fr",
                         help="suffix of French (source language) filename (default=fr)")
    optparser.add_option("-l", "--logfile", dest="logfile", default=None, help="filename for logging output")
    optparser.add_option("-t", "--threshold", dest="threshold", default=0.5, type="float",
                         help="threshold for alignment (default=0.5)")
    optparser.add_option("-n", "--num_sentences", dest="num_sents", default=sys.maxsize, type="int",
                         help="Number of sentences to use for training and alignment")
    (opts, _) = optparser.parse_args()
    f_data = "%s.%s" % (os.path.join(opts.datadir, opts.fileprefix), opts.french)
    e_data = "%s.%s" % (os.path.join(opts.datadir, opts.fileprefix), opts.english)

    if opts.logfile:
        logging.basicConfig(filename=opts.logfile, filemode='w', level=logging.INFO)

    # Translation pairs in the form of a list with two sublist of words
    bitext = [[sentence.strip().split() for sentence in pair] for pair in
              islice(zip(open(f_data), open(e_data)), opts.num_sents)]

    # Train model and get probability distribution
    probabilities = train_alignment(bitext, 20)

    # Get word alignment
    alignment_pos = get_alignment(probabilities, bitext)

    # Save alignments
    for s in alignment_pos:
        for w in s:
            sys.stdout.write("%i-%i " % (w, s[w]))
        sys.stdout.write("\n")

    exit(0)
