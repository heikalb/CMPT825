import os
import csv
import spacy
spacy.load('en_core_web_sm')

nlp = spacy.load('en')

os.chdir("/Users/moarplease/Desktop/nlp-class-hw/cgw")
filename = 'devset.txt'

with open(filename) as f:
    sentences = f.readlines()

tokens = []
lemma = []
pos = []
dep = []

for doc in nlp.pipe(sentences, batch_size=50, n_threads=3):
    if doc.is_parsed:
        tokens.append([n.text for n in doc])
        lemma.append([n.lemma_ for n in doc])
        pos.append([n.pos_ for n in doc])
        dep.append([n.dep_ for n in doc])
    else:
        # to make sure the indices will line up
        tokens.append(None)
        lemma.append(None)
        pos.append(None)
        dep.append(None)


with open("spacy_dep.csv", "w+") as f:
    writer = csv.writer(f)
    for indx, thing in enumerate(dep):
        writer.writerow(tokens[indx])
        writer.writerow(thing)
        writer.writerow(pos[indx])
        writer.writerow(" ")






