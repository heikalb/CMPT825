import tensorflow as tf
import pickle
import argparse
from nltk import word_tokenize
from model import Model
from utils import build_dict, batch_iter, build_dataset_valid_simple, build_prediction

import warnings
warnings.filterwarnings("ignore")

import os
base_path = os.path.dirname(os.path.realpath(__file__))+'/'

def clean_input(input_text):

    clean = " ".join(word_tokenize(input_text.lower()))

    return clean

def summarize_text(input_text,model_name):

    if model_name in ['Sports','Politics','Science']:
        model_name = 'Gigaword'

    text_to_summarize = [clean_input(input_text)]

    model_path = base_path+'saved_model/'+model_name+'/'
    print('\n\nMODEL PATH')
    print(model_path)
    print('\n\n')

    with open(model_path+model_name+"_args.pickle", "rb") as f:
        args = pickle.load(f)

    with open(model_path+"word_dict.pickle", "rb") as f:
        word_dict = pickle.load(f)

    reversed_dict = dict(zip(word_dict.values(), word_dict.keys()))

    article_max_len = 200
    summary_max_len = 50

    valid_x = build_dataset_valid_simple(text_to_summarize,"valid", word_dict, article_max_len, summary_max_len, args.toy)
    valid_x_len = [len([y for y in x if y != 0]) for x in valid_x]

    with tf.Session() as sess:
        print("Loading saved model...")
        model = Model(reversed_dict, article_max_len, summary_max_len, args, forward_only=True)
        saver = tf.train.Saver() #tf.global_variables())
        ckpt = tf.train.get_checkpoint_state(base_path+"saved_model/"+model_name+'/')
        saver.restore(sess, ckpt.model_checkpoint_path)

        batches = batch_iter(valid_x, [0] * len(valid_x), args.batch_size, 1)


        # print("Writing summaries to 'result.txt'...")
        for batch_x, _ in batches:
            batch_x_len = [len([y for y in x if y != 0]) for x in batch_x]

            valid_feed_dict = {
                model.batch_size: len(batch_x),
                model.X: batch_x,
                model.X_len: batch_x_len,
            }

            prediction = sess.run(model.prediction, feed_dict=valid_feed_dict)
            prediction_output = [[reversed_dict[y] for y in x] for x in prediction[:, 0, :]]

            # with open("result.txt", "a") as f:
            for line in prediction_output:
                summary = list()
                for word in line:
                    if word == "</s>":
                        break
                    if word not in summary:
                        summary.append(word)
                # print(" ".join(summary), file=f)

        summary = " ".join(summary)
        print('SUMMARY:',summary)

        sess.close()

        return summary
