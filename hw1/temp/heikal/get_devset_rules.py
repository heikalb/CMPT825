# Get rules from parse trees in devset.trees

from nltk.tree import Tree
from temp.heikal.get_treebank_grammar import get_rules


if __name__ == '__main__':
    # Open devset file
    devset = open('../../devset.trees', 'r').read()[:-1]

    # Separate the trees in the devset, keep track of parentheses
    paren_stack = []
    devset_string = ""

    for ch in devset:
        devset_string += ch

        if ch == '(':
            paren_stack.append('(')
        elif ch == ')' and paren_stack[-1] == '(':
            paren_stack.pop()

        if not paren_stack:
            devset_string += '/#sentboundary#/'

    # Split devset string on boundary symbol
    str_trees = [s for s in devset_string.split('/#sentboundary#/') if not s.isspace()]
    str_trees = [t.replace('\n', '') for t in str_trees]
    trees = []

    # Build trees
    for t in str_trees:
        try:
            trees.append(Tree.fromstring(t))
        # Needed because of a possible quirk with the file
        except ValueError:
            continue

    # Convert trees to CNF
    for t in trees:
        t.chomsky_normal_form()

    # Extract rules and counts (weights)
    rules = [rule for tree in trees for rule in get_rules(tree)]

    # Save data
    with open('devset_rules.txt', 'w') as f:
        f.write('\n'.join(rules))

    exit(0)