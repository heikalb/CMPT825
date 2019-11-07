import perc
import sys, optparse, os
from collections import defaultdict

def perc_train(train_data, tagset, numepochs):
    feat_vec = defaultdict(int)
    sigma_vec = defaultdict(int)
    gamma_vec = defaultdict(int)
    tau_vec = defaultdict(int)
    T = numepochs
    m = len(train_data)

    # Main loop
    for t in range(T):
        print('EPOCH:',t+1)
        mistakes = 0
        
        for i in range(m):
            if i%1000 == 0:
                print(i,end=' ')

            # Get output chunk tags from Viterbi
            labeled_list = train_data[i][0]
            feat_list = train_data[i][1]

            gold_tags = [ll.split()[2] for ll in labeled_list]
            output_tags = perc.perc_test(feat_vec, labeled_list, feat_list, tagset, default_tag=tagset[0])
            
            if t != T-1 & i != m-1:
                
                # Update weight vector if the output is incorrect
                if output_tags != gold_tags:

                    # Get feature IDs: from training data and from Viterbi output
                    feat_ids_gold, feat_ids_output = get_feature_ids(feat_list, gold_tags, output_tags)

                    for k in range(len(gold_tags)):

                        if output_tags[k] != gold_tags[k]:

                            for f in feat_ids_gold[k]:
                                
                                if f in tau_vec.keys():
                                    sigma_vec[f] = sigma_vec[f] + feat_vec[f] * (t * m + i - tau_vec[f][1] * m - tau_vec[f][0])
    
                                feat_vec[f] = feat_vec[f] + 1
                                sigma_vec[f] = sigma_vec[f] + 1
                                # record the location where the dimension tag is updated
                                tau_vec[f] = [i, t]
                                
                            for f in feat_ids_output[k]:
                            
                                if f in tau_vec.keys():
                                    sigma_vec[f] = sigma_vec[f] + feat_vec[f] * (t * m + i - tau_vec[f][1] * m - tau_vec[f][0])
                                    
                                feat_vec[f] = feat_vec[f] - 1
                                sigma_vec[f] = sigma_vec[f] - 1
                                # record the location where the dimension tag is updated
                                tau_vec[f] = [i, t]
                        else:
                            # record the location where the dimension tag is updated
                            for f in feat_ids_gold[k]:
                                tau_vec[f] = [i, t]
                            for f in feat_ids_output[k]:
                                tau_vec[f] = [i, t]

                    mistakes += 1
            else:
               # to deal with the last sentence in the last iteration
               # Get feature IDs: from training data and from Viterbi output
                feat_ids_gold, feat_ids_output = get_feature_ids(feat_list, gold_tags, output_tags)

                for f in tau_vec.keys():
                    sigma_vec[f] = sigma_vec[f] + feat_vec[f] * (T * m + m - tau_vec[f][1] * m - tau_vec[f][0])

                for k in range(len(gold_tags)):
                    if output_tags[k] != gold_tags[k]:
                        for g in feat_ids_gold[k]:
                            feat_vec[g] = feat_vec[g] + 1
                            sigma_vec[g] = sigma_vec[g] + 1
                        for g in feat_ids_output[k]:
                            feat_vec[g] = feat_vec[g] - 1
                            sigma_vec[g] = sigma_vec[g] - 1

        print('\nMistakes in epoch {0}: {1} out of {2} sentences'.format(t+1, mistakes, len(train_data)))
    
    for key in sigma_vec.keys():
        sigma_vec[key] = sigma_vec[key]/(m*T)
        
    return sigma_vec

# Helper function for perc_train. Get feature IDs from a piece of training data.
def get_feature_ids(feat_list, gold_tags, output_tags):
    feat_ids_gold = []
    feat_ids_output = []

    # Get list of list of features - each sublist corresponds to a word
    feat_index = 0
    feat_list_by_words = []
    for i in range(len(gold_tags)):
        (feat_index, feats) = perc.feats_for_word(feat_index, feat_list)
        feat_list_by_words.append(feats)

    # For each feature sublist, create a list of feature IDs ((feature, tag)).
    # One set based on gold tags, another based on argmax tags
    j = 0
    for sublist in feat_list_by_words:
        gold_sublist = []
        out_sublist = []
        for f in sublist:
            # Feature based on bigrams of output tags
            if f == 'B' and j > 0:
                curr_feat_g = '{0}:{1}'.format(f, gold_tags[j - 1])
                curr_feat_o = '{0}:{1}'.format(f, output_tags[j - 1])
            else:
                curr_feat_g = f
                curr_feat_o = f

            gold_sublist.append((curr_feat_g, gold_tags[j]))
            out_sublist.append((curr_feat_o, output_tags[j]))

        feat_ids_gold.append(gold_sublist)
        feat_ids_output.append(out_sublist)

        j += 1

    return feat_ids_gold, feat_ids_output    

if __name__ == '__main__':
    optparser = optparse.OptionParser()
    optparser.add_option("-t", "--tagsetfile", dest="tagsetfile", default=os.path.join("data", "tagset.txt"), help="tagset that contains all the labels produced in the output, i.e. the y in \phi(x,y)")
    optparser.add_option("-i", "--trainfile", dest="trainfile", default=os.path.join("data", "train.txt.gz"), help="input data, i.e. the x in \phi(x,y)")
    optparser.add_option("-f", "--featfile", dest="featfile", default=os.path.join("data", "train.feats.gz"), help="precomputed features for the input data, i.e. the values of \phi(x,_) without y")
    optparser.add_option("-e", "--numepochs", dest="numepochs", default=int(10), help="number of epochs of training; in each epoch we iterate over over all the training examples")
    optparser.add_option("-m", "--modelfile", dest="modelfile", default=os.path.join("data", "default.model"), help="weights for all features stored on disk")
    (opts, _) = optparser.parse_args()

    # each element in the feat_vec dictionary is:
    # key=feature_id value=weight
    feat_vec = {}
    tagset = []
    train_data = []

    tagset = perc.read_tagset(opts.tagsetfile)
    print("reading data ...", file=sys.stderr)
    train_data = perc.read_labeled_data(opts.trainfile, opts.featfile, verbose=False)
    print("done.", file=sys.stderr)
    feat_vec = perc_train(train_data, tagset, int(opts.numepochs))
    perc.perc_write_to_file(feat_vec, opts.modelfile)

