"""
Group and clean articles and summary data in the Opinosis Dataset. For each article there are 3-5 gold summaries.
Each article occurs multiple times in the article file according to how many corresponding reviews there are.

-Heikal Badrulhisham
"""

import os

# Get articles
directory = os.fsencode('../data/OpinosisDataset1.0_0/topics/')
file_list = sorted(os.listdir(directory))
articles = []

for file in file_list:
    file_content = open(os.path.join(directory, file), 'rb').read()

    file_content = str(file_content)
    file_content = file_content.replace('\r', '')
    file_content = file_content.replace('\n', '')
    file_content = file_content.replace('\\r', '')
    file_content = file_content.replace('\\n', '')
    file_content = file_content[2:].strip()

    if file_content.endswith('"'):
        file_content = file_content[:-1]

    articles.append(file_content)

# Get summaries
summaries = []
for i in range(5):
    curr_article_summaries = []
    directory = os.fsencode('../data/OpinosisDataset1.0_0/summaries-gold/')
    subdir_list = sorted(os.listdir(directory))

    for subdir in subdir_list:
        article_subdir = os.fsencode(os.path.join(directory, subdir))

        try:
            summary_file = os.listdir(article_subdir)[i]
        except IndexError:
            curr_article_summaries.append("")
            continue

        file_content = open(os.path.join(article_subdir, summary_file), 'r').read()
        file_content = str(file_content).strip()
        file_content = file_content.replace('\r', '')
        file_content = file_content.replace('\n', '')

        curr_article_summaries.append(file_content)

    summaries.append(curr_article_summaries)


# Multiply number of articles by the number of corresponding summaries
articles_to_save = []
summaries_to_save = []

for i in range(len(articles)):
    for summary in summaries:
        if summary[i]:
            articles_to_save.append(articles[i])
            summaries_to_save.append(summary[i])

article_save_file = open('../data/OpinosisDataset1.0_0/cleaned_data/articles_cleaned.txt', 'w')
summary_save_file = open('../data/OpinosisDataset1.0_0/cleaned_data/summaries_cleaned.txt', 'w')

article_save_file.write('\n'.join(articles_to_save))
summary_save_file.write('\n'.join(summaries_to_save))

print(len(articles_to_save))
print(len(summaries_to_save))
exit(0)