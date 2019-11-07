"""
Clean article and abstract data in the Scisumm dataset and place them in separate files.
"""

# coding: utf-8
import os
from xml.dom import minidom
import xml

art_xmls = []
summary_xmls = []
human_summary_txts = []

articles = []
summaries = []


# Get paths of article XMLs
for r, d, f in os.walk('../data/scisumm-corpus'):
    for f_ in f:
        if '.xml' in f_:
            art_xmls.append(os.path.join(r, f_))
        elif 'human.txt' in f_:
            human_summary_txts.append(os.path.join(r, f_))

# Get abstracts and article contents
for art_xml in art_xmls:
    try:
        ref_xml = minidom.parse(art_xml)
    except xml.parsers.expat.ExpatError:
        print('Parsing error: ', art_xml)
        continue

    # Get article contents
    article_xml = ref_xml.getElementsByTagName('SECTION')
    article_str = ''

    for sect in article_xml:
        sect = sect.getElementsByTagName('S')
        sect_string = ''.join([s.childNodes[0].nodeValue.replace('\n', '').strip() for s in sect])
        article_str += sect_string

    if not article_str:
        continue

    # Get abstracts
    try:
        abstract = ref_xml.getElementsByTagName('ABSTRACT')[0]
        abs_sents = abstract.getElementsByTagName('S')
    except:
        continue

    abs_string = ''.join([s.childNodes[0].nodeValue.replace('\n', '').strip() for s in abs_sents])
    summaries.append(abs_string)
    articles.append(article_str)

    # Get human-made summary if available, duplicate article if there is one
    for human_sum in human_summary_txts:
        if art_xml.split('/')[-1][:-4] in human_sum.split('/')[-1]:
            articles.append(article_str)
            s = str(open(human_sum, 'rb').read()).replace('\n', '').strip()
            summaries.append(s)


# Save data into files
art_save_file = open('../data/scisumm-corpus/cleaned_data/articles_cleaned.txt', 'w')
art_save_file.write('\n'.join(articles))
art_save_file.close()

summary_save_file = open('../data/scisumm-corpus/cleaned_data/abstracts_cleaned.txt', 'w')
summary_save_file.write('\n'.join(summaries))
summary_save_file.close()

print('#Articles: ', len(articles))
print('#Summaries: ', len(summaries))

exit(0)

