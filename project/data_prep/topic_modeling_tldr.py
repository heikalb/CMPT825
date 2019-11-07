import numpy as np
import pandas as pd
pd.set_option('display.max_colwidth', -1)
pd.set_option('display.max_rows', 999)
pd.set_option('display.max_columns', 999)
pd.set_option('display.width', 999)
import glob
import os
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation
from bs4 import BeautifulSoup
from nltk.corpus import stopwords
import warnings
warnings.filterwarnings('ignore')
import re

"""
Summary: Displays all the relevant topics related to a given topic name
"""
def display_relevant_topics(model, feature_names, no_top_words):
    feature_names_list = []
    topic_id_list = []
    for topic_idx, topic in enumerate(model.components_):
        topic_id = topic_idx
        features = ", ".join([feature_names[i]
                        for i in topic.argsort()[:-no_top_words - 1:-1]]) 
        topic_id_list.append(topic_id)
        feature_names_list.append(features)
    
    topic_df = pd.DataFrame({'Topic_ID':topic_id_list,'Topics':feature_names_list})
    return topic_df

for i in range(5,11):
    comments_file = 'data/reddit_tldr/tldr_comments_cleaned_{0}.txt'.format(i)
    model_file = 'data/reddit_tldr/topic_models/tldr_{0}_topics.csv'.format(i)
    
    documents = open(comments_file, 'r')
    no_features = 1000
    no_topics = 10
    no_top_words = 10
    
    tf_vectorizer = CountVectorizer(max_df=0.95, max_features=no_features, stop_words='english', min_df=2)
    tf = tf_vectorizer.fit_transform(documents)
    tf_feature_names = tf_vectorizer.get_feature_names()

    lda = LatentDirichletAllocation(n_components=no_topics, max_iter=5, learning_method='online', learning_offset=50.,random_state=1)
    lda_new = lda.fit(tf)
    lda_topic_df = display_relevant_topics(lda_new, tf_feature_names, no_top_words)
    lda_topic_df.to_csv(model_file)