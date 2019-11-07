import sys, os
#sys.path.append('../model/')
sys.path.append(os.path.join(os.path.dirname(sys.path[0]), 'model'))
from summarize_single import summarize_text

def summarize(text, pretrained_model):
	return summarize_text(text,pretrained_model)
