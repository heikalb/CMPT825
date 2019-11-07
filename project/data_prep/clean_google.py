import json

originals_summaries = []

with open('comp-data.eval.json', 'r') as corpus_file:
    json_strings = corpus_file.read().split('\n\n')

for s in json_strings:
    data = json.loads(s)
    orig = data['graph']['sentence']
    summ = data['compression']['text']
    originals_summaries.append((orig, summ))

j = 0
k = 0

with open('../model/sumdata/google/google_originals.txt', 'w') as f:
    for t in originals_summaries:
        f.write(t[0])
        f.write('\n')
        j += 1
        print('Saving_original:', j)

with open('../model/sumdata/google/google_summaries.txt', 'w') as f:
    for t in originals_summaries:
        f.write(t[1])
        f.write('\n')
        k += 1
        print('Saving_summary:', k)

exit(0)