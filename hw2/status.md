The beam search (using ngram approach) algorithm and helper methods were implemented. However, for now the decipherment being returned map 
symbols only to 'i'. Perhaps the fault lies in the score() function. (Also, the ngram model in baseline_sol.py is set 
to 3 (trigram) to make testing quicker)
-heikal


The beam search with ngram approach is finally returning substantial decipherment. But it is still 
incomprehensible. A notebook version is made as well.
-heikal, 10/09

Fixed the scoring function - needed to include the bitstring of partial decipherment.
Made the pruning function more generalizable.
Previously, the best hypothesis does not map all cipher symbols. Discovered that this can be fixed
by raising ext_limits. This is because the english alphabet has 26 letters but there are 54 cipher symbols.
Thus ext_limits needs to be at least 3 to cover all english letters.
-heikal, 10/10


Simplified code. Added new method of getting the extension order based on Nuhn 2014.
-heikal 10/10

Included initial version of NLM file (nlm_solution_g.py). I'm using the approach from the Thesis "Decipherment of Substitution Ciphers with Neural Language Models", where they map, for each new hypothesis, the characters in the ciphertext correct position (as done by the function g_funct). For the characters not mapped, instead of leaving "_", they do character sampling from the model to complete the sentence. Then, they score the whole sentence with the model. This is taking a huge amount of time, so to try to optimize it, I am scoring the sentence only until the occurrence of at least one of each mapped characters and not the whole sentence.
-gustavo 10/11 7:28pm


Included another test cipher (sandhill_cranes.txt) which is 1-to-1 between cipher and plaintext symbols. The ngram 
solution deciphered it with 100% accuracy.
=heikal 10/12

Tested nlm with part of cipher text "βυρΓϵψσ" from original cipher text ταστωοΣγαηβυρΓϵψσ, output is btbfxny. Chithra - 10/13 2:00 AM

For the nlm_solution, fixed the histogram_prune to return the top-beam best hypothesis for each of the branches of the tree of hypothesis combinations.
-gustavo 10/13

Tested nlm for entire cipher text ταστωοΣγαηβυρΓϵψσ with beam size 2, output is ebdekntlbebbehfyd- Chithra 10/13

Added orthographic constraints on hypothesized decipherment (based vowel/consonant sequence length). Output is still 
incomprehensible but more reasonable-looking.
-heikal 14/10

Tried NLM solution with sampling using the method "next_chars()" from nlm.py. Results not good.
-gustavo 14/10

Implemented the improved get_score using the description in section 5.2 from Improved Decipherment of Homophonic Ciphers. Now the decipherment of the 408-text is taking 2-3 minutes. The results are in part readable, but not similar to the expected plain text.
-gustavo 14/10

Found grounds for previous orthographic constraints. A length constraint of no more than 4 and 5 would cover 99% of 
vowel and consonant sequences (based on the Wikipedia corpus). Improved orthographic constraints. Rather than just measuring the length of vowel/consonant sequences, actual 
vowel/consonant sequences are extracted from the Wikipedia corpus. 
-heikal 14/10

Tested the orthographic constraints on a 1-to-1 cipher and performance deteriorated significantly, 
which is not promising because previously the system was 100% accurate on 1-to-1 cipher.
I have however implemented variable ext_limits. So more common letters are given higher ext_limit
than uncommon ones. The output looks orthographically reasonable
-15/10