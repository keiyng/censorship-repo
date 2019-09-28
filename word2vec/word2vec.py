#import jieba
import re
import logging
import csv
import numpy.linalg as la
#import pandas as pd
import numpy as np
from gensim.models import Word2Vec

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

def main():

    model = load_word2vec_model()
    data = get_data('kindergarten-uncensored-segmented.csv')
    get_word_vectors(model,data)


    #vectors = get_word_vectors(model, data, 'melamine-censored-vectors-mean.csv')

  #  jieba_segmentation_stopwords()


def load_word2vec_model():
    #return KeyedVectors.load_word2vec_format('word2vec.model', binary=False)
    return Word2Vec.load('./model/word2vec.model')

def get_data(csvfile):
    data_list = []
    non_words = re.compile(r'\W')

    with open(csvfile) as data:
        data_text = csv.reader(data)
        for row in data_text:
            for text in row:
                data_list.append(text)

    tokens_list = [data.split(' ') for data in data_list]

    words_list = [[word for word in data if word != '' and not(non_words.match(word))] for data in tokens_list]

    return words_list

#def document_vector(word2vec_model, doc):
#    # remove out-of-vocabulary words
#    doc = [word for word in doc if word in word2vec_model.wv.vocab]
#    return word2vec_model[doc]
#
#    #return np.mean(word2vec_model[doc], axis=0)
#

def get_word_vectors(model, data):
    #vectors = []
    eigenvalues  =[]
    for item in data:# each item is a post
        #print(item)
        # doc is a list of words that appear in the post and match word2vec vocab
        doc = [word for word in item if word in model.wv.vocab]
       # vectors.append(doc)
        vec = model.wv[doc] #get word2vec
        Vector = np.array(vec).T  # transpose
        Vector = Vector.astype(float) # convert values into float
        cov_matrix= np.cov(Vector) # compute covariance matrix
        #evals, evects = la.eig(cov_matrix) # can cause numerical instability
        #print(evals,evects)
        evalsh, evectsh = la.eigh(cov_matrix)#Hermitian
        eigenvalues.append(evalsh)
        #df = pd.DataFrame(evalsh)
    # write into a csv file
    with open("./output/kindergarten-uncensored-eigenvalues2.csv",'w') as resultFile:
        wr = csv.writer(resultFile)
        wr.writerows(eigenvalues)
       # eig_val_cov, eig_vec_cov = np.linalg.eig(cov_matrix)
        #return cov_matrix

#def write_vectors_into_csv(cov_matrix):
#    df = pd.DataFrame(cov_matrix)
#    df.to_csv("covariance.csv", index=False, header=False)
#
#
#def jieba_segmentation_stopwords():
#    seg_data_list = []
#    stopwords_list = []
#
#    with open("zh-wiki-simplified.txt") as data:
#        stopwords = open('stopwords_long.txt')
#        try:
#            stopwords_text = stopwords.read()
#        finally:
#            stopwords.close()
#
#        stopwords_temp_list = stopwords_text.split(',')
#        for item in stopwords_temp_list:
#            item = item.strip()
#            stopwords_list.append(item)
#
#        lines = data.read().splitlines() ##len(lines) == 314510
#
#        for line in lines:
#            segmented_text = jieba.cut(line, cut_all=False, HMM=True)
#            seg_data_list.append(' '.join(segmented_text))
#        seg_data_list = [re.sub( '\s+', ' ', data).strip() for data in seg_data_list]
#        seg_data_list = [data.split(' ') for data in seg_data_list]
#
#        for data in seg_data_list:
#            for word in data:
#                if word in stopwords_list:
#                    data.remove(word)
#
#
#        return seg_data_list
#
##
##def train_word2vec_model(data):
##    print('training model...')
##    model = Word2Vec(data, size=200, window=5, min_count=5, workers=4)
##    print('saving model...')
##    model.save('./model/word2vec.model')
##    model.wv.save_word2vec_format('./model/format', binary=False)
##    print('finished.')
#

if __name__ == '__main__':
    main()
