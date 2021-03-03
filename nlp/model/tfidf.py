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
    def __init__(self, idf_vocab=None):
        self.idf_vocab = idf_vocab
    
    def build_idf_vocab(self, corpus, vocab=None):
        self.idf_vocab = build_idf_vocab(corpus, vocab)
    
    def extract_keyword(self, article, top_n=5, threshold=0.3):
        tf_vocab = get_tf_vocab(article)
        scores = get_tfidf_score(tf_vocab, self.idf_vocab)
        keywords = [word for word, score in scores if score > threshold]
        return keywords[:top_n]
    
# corpus = [
#     'This is the first article about Chinese sports.',
#     'This is the second article about US politics.',
#     'This is the third article about weather.',
#     'This is the fourth article about sports.',
#     'This is the fifth article about election.']
# fw_ex = FreqWordExtract()
# fw_ex.build_idf_vocab(corpus)
# fw_ex.extract_keyword('This document is an article about Chinese politics.')
# output: ['chinese', 'politics']