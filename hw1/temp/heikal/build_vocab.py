# Build vocabulary rules for words in allowed_words.txt

from nltk.corpus import brown
from nltk.corpus import treebank
from nltk.corpus import conll2000
from nltk.corpus import nps_chat
from collections import Counter

import re
remove_suffixes = ['-HL', '-TL', '-NC', '-FM', '-T']


# find tags for a word in a list of trees
def get_tags_trees(word, preterminals):
    tags = []
    for pt in preterminals:
        leaf = [child for child in pt][0]

        if word == leaf:
            tags.append(clean_up(pt.label()))

    return tags


# Find tags associated with a word in a list of tagged words
def get_tags_linear(word, tagged_words):
    return [clean_up(tw[1]) for tw in tagged_words if tw[0] == word]


# Remove from tags suffixes from a prespecified list
def clean_up(tag):
    if tag == 'NP':
        return 'NNP'

    if not re.search(r'[a-zA-Z]', tag):
        return 'Punc-' + tag

    for s in remove_suffixes:
        if s in tag:
            return tag.rstrip(s)

    return tag


# Return the POS of a rule (used for list sorting)
def get_key(rule):
    return rule.split()[1]


if __name__ == '__main__':
    # Get allowed words
    allowed_words_file = open('../../allowed_words.txt', 'r')
    allowed_words = allowed_words_file.read().split('\n')

    # Tagged words from corpora
    treebank_tagged_words = list(set(treebank.tagged_words()))
    conll2000_tagged_words = list(set(conll2000.tagged_words()))
    brown_tagged_words = list(set(brown.tagged_words()))
    nps_tagged_words = list(set(nps_chat.tagged_words()))

    vocab_rules = []
    unvocabbed_words = []

    # Find tags that occur with allowed words in the corpora
    for word in allowed_words:
        curr_tags = get_tags_linear(word, treebank_tagged_words)

        if not curr_tags:
            curr_tags = get_tags_linear(word, conll2000_tagged_words)

        if not curr_tags:
            curr_tags = get_tags_linear(word, brown_tagged_words)

        if not curr_tags:
            curr_tags = get_tags_linear(word, nps_tagged_words)

        # Add vocab rules, or list the word as unvocabbed
        if curr_tags:
            tag_count = Counter(curr_tags)
            vocab_rules += ['{0:10s}{1:13s}{2}'.format(str(tag_count[k]), k, word) for k in tag_count]
        else:
            unvocabbed_words.append('{0:10s}{1:13s}{2}'.format(str(1), 'Misc', word))

    # Get manually written vocab rules
    with open('manual_vocab.txt', 'r') as f:
        vocab_rules = vocab_rules + f.read().split('\n')

    # Clean up rule list
    vocab_rules = list(set(vocab_rules))
    vocab_rules.sort(key=get_key)

    # Save data
    with open('Vocab-h.gr', 'w') as f:
        f.write('\n'.join(vocab_rules))

    with open('unvocabbed_words.txt', 'w') as f:
        f.write('\n'.join(unvocabbed_words))

    print('\a')
    exit(0)
