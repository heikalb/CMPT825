# Gustavo Felhberg

## Last updates:

#### File **build_vocabulary.ipynb**:

Obs: Using version started by Heikal.

Current state: 
- Extract the words and respectives POS and number of occurrences in the corpus
- Filter out words that are not in the allowed_words.txt file

Outputs: **newvocab.txt** and **unassigned_words.txt**

#### File **get_grammar.ipynb**:

Obs: Using version started by Heikal.

Current state: 
- Extracts grammar from treebank corpus from NLTK
- Counts the number of occurrences of each rule in the corpus and save it in the output file
- Adds initial rule "1 TOP S" to grammar

Output: **probabilistic_grammar.txt** 

#### File **sentences_to_validate.txt**:

Examples of simple sentences to be used to validate the grammar

## Next Steps:

- extract vocabulary from multiple corpus
- get words in allowed_words.txt not identified by the build_vocabulary script, extract its POS and add to the vocabulary file

## To Test:

run **python3 pcfg_parse_gen.py -g probabilistic_grammar.txt newvocab.txt -i < sentences_to_validate.txt**




