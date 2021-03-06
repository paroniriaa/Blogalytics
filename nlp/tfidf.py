import os
import json
import random
import logging
from collections import Counter
import pickle as pkl

import numpy as np
from sklearn.feature_extraction.text import CountVectorizer


def build_idf_vocab(corpus, vocabulary=None):
    vectorizer = CountVectorizer(vocabulary=vocabulary)
    matrix = vectorizer.fit_transform(corpus)
    count = (matrix.toarray() > 0).sum(axis=0)
    words = vectorizer.get_feature_names()
    idf_vocab = {}
    for word, c in zip(words, count):
        idf_vocab[word] = np.log(len(corpus)/c )
    return idf_vocab

def get_tf_vocab(article):
    assert type(article) == str, "article must be in string format"
    vectorizer = CountVectorizer()
    count = vectorizer.fit_transform([article]).toarray()[0]
    words = vectorizer.get_feature_names()
    tf_vocab = {}
    for word, freq in zip(words, count):
        tf_vocab[word] = freq
    return tf_vocab

def get_tfidf_score(tf_vocab, idf_vocab):
    scores = []
    for word in tf_vocab:
        tfidf = tf_vocab[word] * idf_vocab.get(word, 0)
        scores.append([word, tfidf])
    scores = sorted(scores, key=lambda x: x[1], reverse=True)
    return scores


class FreqWordExtract():
    def __init__(self, idf_vocab):
        self.idf_vocab = idf_vocab

    def extract_keyword(self, article, top_n=5, threshold=0.3):
        tf_vocab = get_tf_vocab(article)
        scores = get_tfidf_score(tf_vocab, self.idf_vocab)
        keywords = [word for word, score in scores if score > threshold]
        return keywords[:top_n]


def read_lines(filename):
    with open(filename) as file:
        lines = file.readlines()
    lines = [line.strip('\n') for line in lines]
    return lines

def extract_from_json(json_str, verbose=False):
    src = []
    tgt = []
    for idx in range(len(json_str)):
        if idx % 1000 == 0:
            if verbose:
                logging.info('processing idx: ', idx)
        data = json.loads(json_str[idx])
        article = data['abstract']
        keyword = data['keyword']
        keyword = keyword.split(';')
        src.append(article)
        tgt.append(keyword)
    return src, tgt


# setup keyword_extract

def setup_idf_vocab(
    idf_vocab_pkl_path = 'nlp/data/idf_vocab.pkl',
    corpus_path = 'nlp/data/KPTimes.test.jsonl'):

    if os.path.exists(idf_vocab_pkl_path):
        with open(idf_vocab_pkl_path, 'rb') as file:
            idf_vocab = pkl.load(file)
        logging.info('idf vocab loaded')
    else:
        logging.info('idf vocab pickle file not found, building from scratch...')
        lines = read_lines(corpus_path)
        corpus, keywords = extract_from_json(lines)
        idf_vocab = build_idf_vocab(corpus)
        logging.info('build idf vocab successfully')
        logging.info('saving idf vocab to {}'.format(idf_vocab_pkl_path))
        with open(idf_vocab_pkl_path, 'wb') as file:
            pkl.dump(idf_vocab, file)

    return idf_vocab


# idf_vocab = setup_idf_vocab()
# extractor = FreqWordExtract(idf_vocab=idf_vocab)
# extractor.extract_keyword('This is the first article about Chinese sports.')
