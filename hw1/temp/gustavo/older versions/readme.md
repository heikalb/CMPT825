#Heikal Badrulhisham

##Vocbulary building
Assign every word in allowed_words.txt a vocabulary rule. 
Brown corpus was used to find the possible POS tags of each word.
If that fails, NLTK's Wordnet was used.
For now each vocabulary rule is assigned a weight of 1.
Words that were not assigned a rule were stored separately.

Used: build_vocab.py
Output: Vocab-h.gr, unvocabbed_words.txt

##Get grammar rules
The (sample of) Penn Treebank was used to obtain rules of the grammar.
For now each grammar rule is assigned a weight of 1.

Used: get_treebank_grammar.py
Output: S2-h.gr

##Manual vocabbing
Word that could not be assigned a vocabulary rule were assigned manually. These rules were added to Vocab-h.gr

##Cleaning S2 grammar
Nodes that do not have a role were deleted. These include nodes for the dollar sign, '$', and -NONE- nodes

##S1 tweak
The weights of the TOP rules were shifted in favor of S2