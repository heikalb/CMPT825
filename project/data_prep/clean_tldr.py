import json

comment_tldrs = []


with open('../data/reddit_tldr/tldr-training-data.jsonl', 'r') as corpus_file:
    i = 0

    for line in corpus_file:
        curr_json = json.loads(line)
        comment_tldrs.append((curr_json['content'], curr_json['summary']))

        i += 1
        if i%100000 == 0:
            print(i)

divider = int(len(comment_tldrs)/5)

for i in range(5):
    with open('../data/reddit_tldr/tldr_comments_cleaned_{0}.txt'.format(i+1), 'w') as f:
        for t in comment_tldrs[divider*i:divider*(i+1)]:
            f.write(t[0].replace('\n', ''))
            f.write('\n')

    with open('../data/reddit_tldr/tldr_summaries_cleaned_{0}.txt'.format(i+1), 'w') as f:
        for t in comment_tldrs[divider*i:divider*(i+1)]:
            f.write(t[1])
            f.write('\n')

exit(0)