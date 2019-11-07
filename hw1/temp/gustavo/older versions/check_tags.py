# Go through Penn Treebank to find examples of subtrees with a given tag or word - for verifying denotation of tags or
# finding tags associated with a word

from nltk.corpus import treebank


# show subtrees in a tree with a given tag
def show_tag(tree, tag):
    subtrees = tree.subtrees()

    for subtree in subtrees:
        if subtree.label() == tag:
            print(tree)


# show subtrees in a tree with a given word
def show_word(tree, word):
    subtrees = tree.subtrees()

    for subtree in subtrees:
        if [c for c in subtree][0] == word:
            print(subtree)


if __name__ == '__main__':
    # get trees for Penn Treebank
    trees_by_file = [treebank.parsed_sents(id) for id in treebank.fileids()]
    trees = [tree for files in trees_by_file for tree in files]

    # go through trees, look for occurrences
    for tree in trees:
        show_word(tree, 'morning')
        #show_tag(tree, 'UH')

