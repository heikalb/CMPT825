# Get grammatical rules from syntactic trees in a sample of the Penn Treebank
from nltk.corpus import treebank
from collections import Counter
import re
unneeded_nodes = [' $ ', '-$', '-NONE-', '#']


def get_rules(tree):
    # Get subtrees of the tree
    subtrees = tree.subtrees()
    rules = []

    # For each subtree get the rule that generates it's immediate child node
    for subtree in subtrees:
        children = [ch for ch in subtree]

        # Skip nodes that lead to leaves
        if len(children) > 0 and not type(children[0]) == str:
            # get labels of child nodes
            child_labels = [fix_label(ch.label()) for ch in children]

            # create rule string
            curr_rule = '\t'.join([fix_label(subtree.label())] + child_labels)
            rules.append(curr_rule)

    return rules


def fix_label(label):
    if not re.search(r'[a-zA-Z]', label):
        return 'Punc-' + label
    if label == 'S':
        return 'S2'

    return label


def exclude_rule(rule):
    for n in unneeded_nodes:
        if n in rule:
            return True

    return False


if __name__ == '__main__':
    # get trees for Penn Treebank
    trees_by_file = [treebank.parsed_sents(id) for id in treebank.fileids()]
    trees = [tree for files in trees_by_file for tree in files]

    # Convert trees to CNF
    for i in range(len(trees)):
        tree = trees[i]
        tree.chomsky_normal_form()

    # Collect rules from treebank
    rules = [rule for tree in trees for rule in get_rules(tree) if not exclude_rule(rule)]

    # Get devset rules
    rules += open('devset_rules.txt', 'r').read().split('\n')

    # Replace cycles
    rules = [r for r in rules if not (len(r.split()) == 2 and r.split()[0] == r.split()[1])]

    rule_counts = Counter(rules)
    rules = list(set(rules))
    rules.sort()

    # Add misc rules
    misc_rules = open('misc_rules.txt', 'r').read().split('\n')

    # Save rules into grammar file
    with open('S2-h.gr', 'w') as f:
        f.write('# Number of rules: {0}\n'.format(len(rules) + len(misc_rules)))

        for r in rules:
            f.write('{0}\t\t{1}\n'.format(rule_counts[r], r))
        for r in misc_rules:
            f.write(r + '\n')

    exit(0)
