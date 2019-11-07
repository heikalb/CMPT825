# For running parsing or generating tests

from pcfg_parse_gen import Pcfg, PcfgGenerator, CkyParse
import nltk


def print_tree(tree_string):
    tree_string = tree_string.strip()
    tree = nltk.Tree.fromstring(tree_string)
    tree.pretty_print()


def draw_tree(tree_string):
    tree_string = tree_string.strip()
    tree = nltk.Tree.fromstring(tree_string)
    tree.draw()


# Parsing
parse_gram = Pcfg(["temp/heikal/S1-h.gr","temp/heikal/S2-h.gr","temp/heikal/Vocab-h.gr"])
#parse_gram = Pcfg(["S1.gr", "S2.gr", "Vocab.gr"])

parser = CkyParse(parse_gram, beamsize=0.00001)
ce, trees = parser.parse_sentences(["Arthur is the king ."])
print("-cross entropy: {}".format(ce))
for tree_string in trees:
    print_tree(tree_string)

ce, trees = parser.parse_sentences(["five strangers are at the Round Table ."])
print("-cross entropy: {}".format(ce))
for tree_string in trees:
    print_tree(tree_string)

ce, trees = parser.parse_file('example_sentences.txt')
#ce, trees = parser.parse_file('devset.txt')
print("-cross entropy: {}".format(ce))

"""
# Generate

gen_gram = Pcfg(["temp/heikal/S1-h.gr","temp/heikal/Vocab-h.gr"])
#gen_gram = Pcfg(["S1.gr","Vocab.gr"])

gen = PcfgGenerator(gen_gram)
for _ in range(20):
    print(" ".join(gen.generate()))
"""