import os
import json
import random
import logging
from collections import Counter
import pickle as pkl

import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
import langdetect

from spacy.lang.ja import Japanese
from spacy.lang.zh import Chinese


jp_nlp = Japanese()
# Jieba
cn_cfg = {"segmenter": "jieba"}
cn_nlp = Chinese.from_config({"nlp": {"tokenizer": cn_cfg}})


def build_idf_vocab(corpus):
    """Build the inverse document frequency(idf) dictionary

    :param corpus: a list of string represent the articles to generate idf dict

    :returns: a dict that maps a word to its idf value
    :rtype: dict(string, float)
    """

    vectorizer = CountVectorizer(vocabulary=None)
    matrix = vectorizer.fit_transform(corpus)
    count = (matrix.toarray() > 0).sum(axis=0)
    words = vectorizer.get_feature_names()
    idf_vocab = {}
    for word, c in zip(words, count):
        idf_vocab[word] = np.log(len(corpus)/c )
    return idf_vocab

def get_tf_vocab(article):
    """Build the term frequency(tf) dictionary for a given article

    :param article: a string, representing the article

    :returns: a dict that maps a word to its tf value
    :rtype: dict(string, float)
    """
    assert type(article) == str, "article must be in string format"
    vectorizer = CountVectorizer()
    count = vectorizer.fit_transform([article]).toarray()[0]
    words = vectorizer.get_feature_names()
    tf_vocab = {}
    for word, freq in zip(words, count):
        tf_vocab[word] = freq
    return tf_vocab

def get_tfidf_score(tf_vocab, idf_vocab):
    """Calculate the tfidf score for an article

    :param tf_vocab: a dict that maps a word into its tf value
    :param idf_vocab: a dict that maps a word into its idf value

    :returns: a list of tuple, where the first element is the word,
              the second element is its tf-idf score.
    :rtype: a list of (str, float)
    """

    scores = []
    for word in tf_vocab:
        tfidf = tf_vocab[word] * idf_vocab.get(word, 0)
        scores.append([word, tfidf])
    scores = sorted(scores, key=lambda x: x[1], reverse=True)
    return scores


class FreqWordExtract():
    def __init__(self, idf_vocab_dict):
        self.idf_vocab_dict = idf_vocab_dict

    def extract_keyword(self, article, top_n=5, threshold=0.3):
        """Extract keywords from an article based on tf-idf algorithm

        :param: article: a string representing the article
        :param: top_n: output top_n keywords sorted by their tf-idf value
        :param: threshold: only keywords whose scores are above threshold
                chosen as output

        :returns: a list of string, each element is a generated keyword
        :rtype: a list of string
        """
        lang_type = langdetect.detect(article)
        if 'cn' in lang_type:
            tokens = tokenize_w_spacy(article, cn_nlp)
            article = ' '.join(tokens)
            idf_vocab = self.idf_vocab_dict['cn']
        elif 'ja' in lang_type:
            tokens = tokenize_w_spacy(article, jp_nlp)
            article = ' '.join(tokens)
            idf_vocab = self.idf_vocab_dict['jp']
        else:
            idf_vocab = self.idf_vocab_dict['en']

        tf_vocab = get_tf_vocab(article)
        scores = get_tfidf_score(tf_vocab, idf_vocab)
        keywords = [word for word, score in scores if score > threshold]
        return keywords[:top_n]


def read_lines(filename):
    with open(filename) as file:
        lines = file.readlines()
    lines = [line.strip('\n') for line in lines]
    return lines

def extract_english_corpus(json_str, verbose=False):
    """A helper function to extract English corpus from KPTimes dataset in json

    :param: json_str: the json string
    :param: verbose: bool, if logging the process of data processing

    :returns: the articles and keywords for each article
    :rtype: src (list of string), tgt (list of keyword list)
    """
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


def extract_chinese_corpus(raw_lines):
    """A helper function to extract Chinese corpus

    :param: json_str: the json string

    :returns: the articles and keywords for each article
    :rtype: corpus (list of string)"""
    corpus = []
    article = []
    for line in raw_lines:
        idx = int(line.split(' ')[0])
        sent = line.split(' ||| ')[1]
        if idx == 1:
            if article:
                corpus.append(article)
            article = sent
        else:
            article += sent
        if len(corpus) > 30000:
            break
    return corpus

def tokenize_w_spacy(article, language_nlp):
    tokens = []
    doc = language_nlp(article)
    for w in doc:
        tokens.append(w.text)
    return tokens

# setup idf vocab for keyword extraction
# Source for the English corpus we used: https://github.com/ygorg/KPTimes
en_corpus_path = 'nlp/data/KPTimes.test.jsonl'
en_idf_pkl_path = 'nlp/data/en_idf_vocab.pkl'

# The Chinese raw corpus file is too large
# Thus, we only upload the necessary processed data in the repo
# Raw corpus is available at: https://github.com/ymcui/Chinese-Cloze-RC/tree/master/people_daily
cn_corpus_path = 'nlp/data/pd/pd.train'
cn_idf_pkl_path = 'nlp/data/cn_idf_vocab.pkl'

# Source for the Japanese corpus we used: https://github.com/wikiwikification/jawikicorpus
jp_corpus_path = 'nlp/data/jawikicorpus.20181120.small.txt'
jp_idf_pkl_path = 'nlp/data/jp_idf_vocab.pkl'


def setup_idf_vocab():
    lang2pkl_path = {
        'en': en_idf_pkl_path,
        'cn': cn_idf_pkl_path,
        'jp': jp_idf_pkl_path}
    lang2corpus_path = {
        'en': en_corpus_path,
        'cn': cn_corpus_path,
        'jp': jp_corpus_path}

    output_tfidf_dict = {}

    for language in ['en', 'cn', 'jp']:
        pkl_path = lang2pkl_path[language]
        if os.path.exists(pkl_path):
            with open(pkl_path, 'rb') as file:
                idf_vocab = pkl.load(file)
            logging.info('idf vocab loaded')
        else:
            logging.info('idf vocab pickle file not found, building from scratch...')
            raw_lines = read_lines(en_corpus_path)
            if language == 'en':
                corpus, keywords = extract_english_corpus(raw_lines)
            elif language == 'cn':
                corpus = extract_chinese_corpus(raw_lines)
            elif language == 'jp':
                raw_corpus = raw_lines
                corpus = []
                for article in raw_corpus:
                    tokens = tokenize_w_spacy(article, jp_nlp)
                    corpus.append(' '.join(tokens))
            idf_vocab = build_idf_vocab(corpus)
            logging.info('build idf vocab successfully')
            logging.info('saving idf vocab to {}'.format(idf_vocab_pkl_path))
            with open(pkl_path, 'wb') as file:
                pkl.dump(idf_vocab, file)
        print(language, len(idf_vocab))
        output_tfidf_dict[language] = idf_vocab

    return output_tfidf_dict


# idf_vocab_dict = setup_idf_vocab()
# extractor = FreqWordExtract(idf_vocab_dict)
# extractor.extract_keyword('This is the first article about Chinese sports.')
