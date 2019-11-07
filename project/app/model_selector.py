import pickle
import nltk
import spacy
from nltk.corpus import stopwords
from nltk import RegexpTokenizer

print('Loading language model...')
nlp = spacy.load('en_core_web_sm')

print('Loading stopwords...')
nltk.download('stopwords')

corpus_cnn      = pickle.load( open( "../text_similarity/corpus_cnn.pkl", "rb" ) )
corpus_daily    = pickle.load( open( "../text_similarity/corpus_dailymail.pkl", "rb" ) )
corpus_sports   = pickle.load( open( "../text_similarity/corpus_sports.pkl", "rb" ) )
corpus_politics = pickle.load( open( "../text_similarity/corpus_politics.pkl", "rb" ) )
corpus_science  = pickle.load( open( "../text_similarity/corpus_science.pkl", "rb" ) )


tokenizer = RegexpTokenizer(r'\w+')
stopword_set = set(stopwords.words('english'))

def nlp_clean(data):
    new_data = []
    new_str = data.lower()
    dlist = tokenizer.tokenize(new_str)
    dlist = list(set(dlist).difference(stopword_set))
    new_data.append(dlist)
    return dlist

def get_similarity(text1, text2):
    return nlp(' '.join(nlp_clean(text1))).similarity(nlp(' '.join(nlp_clean(text2))))

def get_best_model(text):

	best_similarity=0
	best_model=''
	for model in models_to_evaluate.keys():
		sim = get_similarity(text,models_to_evaluate[model])
		if sim > best_similarity:
			best_similarity = sim
			best_model = model
	return best_model, best_similarity

models_to_evaluate = {
    'CNN_News':corpus_cnn,
    'DailyMail':corpus_daily,
    'Sports':corpus_sports,
    'Politics':corpus_politics,
    'Science':corpus_science,
}