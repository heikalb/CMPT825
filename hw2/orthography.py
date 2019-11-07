# Script for deriving constraints based on English orthography

from collections import Counter
import sys
sys.path.append('../')
from ngram import *
from nltk.util import ngrams


def read_file(filename):
    if filename[-4:] == ".bz2":
        with bz2.open(filename, 'rt') as f:
            content = f.read()
            f.close()
    else:
        with open(filename, 'r') as f:
            content = f.read()
            f.close()
    return content


wiki = read_file("data/default.wiki.txt.bz2").replace('\n', '')
vowels = 'aeiou'
cons = 'tnshrdlcmwfgypbvkjxqz'
vowel_spans = ''
cons_spans = ''

for c in wiki:
    if c in vowels:
        vowel_spans += c
    else:
        vowel_spans += '#'

for c in wiki:
    if c in cons:
        cons_spans += c
    else:
        cons_spans += '#'


vowel_spans = Counter([len(s) for s in vowel_spans.split('#') if len(s) > 0])
cons_spans = Counter([len(s) for s in cons_spans.split('#') if len(s) > 0])

print(sum([vowel_spans[k] for k in vowel_spans])*0.99)
print(sum([cons_spans[k] for k in cons_spans])*0.99)

cum = 0
for k in vowel_spans.most_common():
    cum += k[1]
    print(k, cum)

print('\n\n')

cum = 0
for k in cons_spans.most_common():
    cum += k[1]
    print(k, cum)

