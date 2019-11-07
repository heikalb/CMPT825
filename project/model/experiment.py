import sys
sys.path.append('../')
sys.path.append('../../app/')
import summarize_single
import app.model_selector as model_selector
from rouge import Rouge

# Get test data
originals = open('sumdata/google/google_originals.txt', 'r').read().split('\n')
summaries = open('sumdata/google/google_summaries.txt', 'r').read().split('\n')
pairs = [(originals[i], summaries[i]) for i in range(len(originals))]

# For scoring summaries
rouge = Rouge()


# Experimental condition 1: one model system
rouge_scores_1 = {'rouge-1': {'f': 0, 'p': 0, 'r': 0}, 'rouge-2': {'f': 0, 'p': 0, 'r': 0},
                  'rouge-l': {'f': 0, 'p': 0, 'r': 0}}

for pair in pairs:
    output_summary = summarize_single.summarize_text(pair[0], 'Gigaword')
    rouge_score = rouge.get_scores(output_summary, pair[1])

    for r in rouge_scores_1:
        for r_ in rouge_scores_1[r]:
            rouge_scores_1[r][r_] += rouge_score[0][r][r_]

# Experimental condition 2: multiple model system
rouge_scores_2 = {'rouge-1': {'f': 0, 'p': 0, 'r': 0}, 'rouge-2': {'f': 0, 'p': 0, 'r': 0},
                  'rouge-l': {'f': 0, 'p': 0, 'r': 0}}

for pair in pairs:
    selected_model = model_selector.get_best_model(pair[0])
    output_summary = summarize_single.summarize_text(pair[0], selected_model[0])
    rouge_score = rouge.get_scores(output_summary, pair[1])

    for r in rouge_scores_2:
        for r_ in rouge_scores_2[r]:
            rouge_scores_2[r][r_] += rouge_score[0][r][r_]


print('Average score in condition 1:')
for r in rouge_scores_1:
    for r_ in rouge_scores_1[r]:
        print('{0} {1}: {2}'.format(r, r_, rouge_scores_1[r][r_]/len(pairs)))
        rouge_scores_1[r][r_]

print('Average score in condition 2: ')
for r in rouge_scores_2:
    for r_ in rouge_scores_2[r]:
        print('{0} {1}: {2}'.format(r, r_, rouge_scores_2[r][r_]/len(pairs)))
        rouge_scores_2[r][r_]

exit(0)