# Implementation of baseline solution (beam_search) Some of the code here is from the default notebook.
from collections import Counter
import sys
sys.path.append('../')
from ngram import *
from nltk.util import ngrams

# ngram model for scoring hypotheses
ngram_model = LM("data/6-gram-wiki-char.lm.bz2", n=6, verbose=False)


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


# Beam search algorithm
def beam_search(plaintext_alph, cipher_text, ext_order, ext_limits=1, beam_size=1):
    # partial hypotheses
    scored_hypotheses = [(0, [])]
    hypothesis_extensions = []

    for cipher_sym in ext_order:
        for hyp in scored_hypotheses:
            for pl_sym in plaintext_alph:
                new_hypothesis = hyp[1] + [(pl_sym, cipher_sym)]

                if within_ext_limits(ext_limits, new_hypothesis):
                    hypothesis_extensions.append((score(new_hypothesis, cipher_text), new_hypothesis))

            if hypothesis_extensions:
                hypothesis_extensions = histogram_prune(hypothesis_extensions, beam_size)
                scored_hypotheses = [h for h in hypothesis_extensions]

        hypothesis_extensions.clear()
    return winning_hypothesis(scored_hypotheses)


def _beam_search(plaintext_alph, cipher_text, ext_order, ext_limits=1, beam_size=1):
    # partial hypotheses
    scored_hypotheses = [(0, []), (0, [('e', '-')])]
    hypothesis_extensions = []

    b = beam_size*10

    for cipher_sym in ext_order:
        if b < beam_size:
            b = beam_size

        for hyp in scored_hypotheses:
            for pl_sym in plaintext_alph:
                new_hypothesis = hyp[1] + [(pl_sym, cipher_sym)]

                if within_ext_limits(ext_limits, new_hypothesis):
                    hypothesis_extensions.append((score(new_hypothesis, cipher_text), new_hypothesis))

            if hypothesis_extensions:
                hypothesis_extensions = histogram_prune(hypothesis_extensions, b)
                scored_hypotheses = [h for h in hypothesis_extensions]
        b -= 3
        hypothesis_extensions.clear()
    return winning_hypothesis(scored_hypotheses)


# If the hypothesis exceeds the constraint on many-to-one mapping
def within_ext_limits(limit, hyp):
    plaintxt_sym_counter = Counter([tup[0] for tup in hyp])
    return not any(plaintxt_sym_counter[k] > limit[k] for k in plaintxt_sym_counter)


# Hypothesis scoring function
def score(hypothesis, text):
    decipherment = ''.join([g_funct(hypothesis, ch) for ch in text])
    bitstring = ''
    for ch in decipherment:
        if ch == '_':
            bitstring += '.'
        else:
            bitstring += 'o'
    return ngram_model.score_bitstring(decipherment, bitstring)


# Returns plaintext string for a cipher symbol given a hypothesized mapping
def g_funct(hypothesis, cipher_sym):
    for tup in hypothesis:
        if tup[1] == cipher_sym:
            return tup[0]
    return '_'


# Returns a sublist of n best scoring hypotheses
def histogram_prune(hypotheses, n=1):
    hypotheses.sort(reverse=True)
    return hypotheses[:n]


# Returns the best hypothesis
def winning_hypothesis(hypotheses):
    return histogram_prune(hypotheses, 1)[0][1]


# Get an extension order based on contiguous deciphered ngrams
def get_ext_order(alphabet, cipher):
    ext_order = [alphabet[0]]
    alphabet.pop(0)

    while alphabet:
        max_sum = weighted_sum(alphabet[0], cipher, ext_order)
        max_char = alphabet[0]

        for a in alphabet[1:]:
            curr_sum = weighted_sum(a, cipher, ext_order)

            if curr_sum > max_sum:
                max_sum = curr_sum
                max_char = a

        ext_order.append(max_char)
        alphabet.remove(max_char)

    return ext_order


# Calculate the weighted sum for ext order candidates
def weighted_sum(ch, cipher, ext_order):
    sum = 0
    for n in range(2, 7):
        grams = [g for g in ngrams(cipher, n) if all(c in ext_order + [ch] for c in g)]
        sum += len(grams) * n

    return sum


def read_gold(gold_file):
    with open(gold_file) as f:
        gold = f.read()
    f.close()
    gold = list(gold.strip())
    return gold


def symbol_error_rate(dec, _gold):
    gold = read_gold(_gold)
    correct = 0
    if len(gold) == len(dec):
        for (d, g) in zip(dec, gold):
            if d == g:
                correct += 1
    wrong = len(gold) - correct
    error = wrong / len(gold)

    return error


if __name__ == '__main__':
    # Cipher and plaintext files
    cipher = read_file("data/cipher.txt").replace('\n', '')
    # cipher = read_file("sandhill_cranes.txt").replace('\n', '')
    plaintxt = read_file("data/default.wiki.txt.bz2")

    # Cipher and plaintext alphabets
    cipher_count = Counter([ch for ch in cipher if not ch == '\n'])
    # Order cipher letters to maximize contiguous ngrams for each partial hypothesis
    ext_order = [tup[0] for tup in cipher_count.most_common()]
    ext_order = get_ext_order(ext_order, cipher)
    # English alphabet ordered by letter frequency
    eng_alphabet = [ch for ch in 'etaoinshrdlcumwfgypbvkjxqz']

    # Variable Extension limits for each plaintext letter, last one simulates fixed extension limits
    ext_limit = {'e': 4, 't': 3, 'a': 3, 'o': 3, 'i': 3, 'n': 2, 's': 2, 'h': 2, 'r': 2, 'd': 2,
                 'l': 2, 'c': 2, 'u': 2, 'm': 2, 'w': 1, 'f': 1, 'g': 1, 'y': 1, 'p': 1, 'b': 1,
                 'v': 1, 'k': 1, 'j': 1, 'x': 1, 'q': 1, 'z': 1}

    ext_limit_2 = {'e': 8, 't': 8, 'a': 8, 'o': 6, 'i': 6, 'n': 6, 's': 6, 'h': 6, 'r': 6, 'd': 4,
                   'l': 4, 'c': 4, 'u': 4, 'm': 4, 'w': 4, 'f': 4, 'g': 4, 'y': 4, 'p': 4, 'b': 4,
                   'v': 2, 'k': 2, 'j': 2, 'x': 2, 'q': 2, 'z': 2}

    ext_limit_3 = {'e': 4, 't': 4, 'a': 3, 'o': 3, 'i': 3, 'n': 3, 's': 3, 'h': 3, 'r': 3, 'd': 2,
                   'l': 2, 'c': 2, 'u': 2, 'm': 2, 'w': 2, 'f': 2, 'g': 2, 'y': 2, 'p': 2, 'b': 2,
                   'v': 2, 'k': 2, 'j': 2, 'x': 2, 'q': 2, 'z': 2}

    e = 6
    ext_limit_4 = {'e': e, 't': e, 'a': e, 'o': e, 'i': e, 'n': e, 's': e, 'h': e, 'r': e, 'd': e,
                   'l': e, 'c': e, 'u': e, 'm': e, 'w': e, 'f': e, 'g': e, 'y': e, 'p': e, 'b': e,
                   'v': e, 'k': e, 'j': e, 'x': e, 'q': e, 'z': e}

    # Get the best decipherment hypothesis
    best_hypothesis = beam_search(eng_alphabet, cipher, ext_order, ext_limit_4, 26)
    # Decipher cipher text
    decipherment = ''.join([g_funct(best_hypothesis, ch) for ch in cipher])

    print(best_hypothesis)
    print(decipherment)

    # Evaluate accuracy
    gold_file = "data/_ref.txt"
    ser = symbol_error_rate(decipherment, gold_file)
    print('Error: ', ser * 100, 'Accuracy: ', (1 - ser) * 100)

    exit(0)