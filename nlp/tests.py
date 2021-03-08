import os

from django.test import TestCase
from nlp.tfidf import *
from nlp.word_cloud import *


class BuildIdvVocabTests(TestCase):

    def test_build_idf_vocab(self):
        out_dict = build_idf_vocab(corpus=[
            'hi world',
            'hi mick',
            'hi, this is a long long long long sentence'])
        self.assertEqual(out_dict['hi'], 0.0)
        self.assertEqual(out_dict['world'], out_dict['mick'])

    def test_get_tf_vocab(self):
        tf_vocab = get_tf_vocab("Hello world this is a testing article for testing")
        self.assertEqual(tf_vocab.get('world', 0), 1)
        self.assertEqual(tf_vocab.get('testing', 0), 2)
        self.assertEqual(tf_vocab.get('not-exists', 0), 0)
        self.assertEqual(len(tf_vocab), 7)

    def test_get_tfidf_score(self):
        tf_vocab = {'a': 0.1, 'b': 0.3, 'c': 0.5}
        idf_vocab = {'a': 0.1, 'b': 2.0, 'd': 1.0}
        out = get_tfidf_score(tf_vocab, idf_vocab)
        self.assertEqual(out[0][0], 'b')
        self.assertEqual(out[1][0], 'a')
        self.assertEqual(out[2][0], 'c')
        self.assertEqual(out[2][1], 0)

    def test_load_idf_vocab_from_pkl(self):
        vocab = setup_idf_vocab()
        self.assertEqual(len(vocab)>0, True)


class WordCloudTests(TestCase):

    def test_remove_stop_words(self):
        article = 'i am a stop words, but book is not'
        filtered_tokens = remove_stop_words(article)
        # only non-stops words are 'stop', 'words', 'book'
        self.assertEqual(len(filtered_tokens), 3)

    def test_plot_a_figure(self):
        # build a empty folder for testing
        folder_dir = 'test_tmp'
        if not os.path.exists(folder_dir):
            os.makedirs(folder_dir)
        article = "Python is an interpreted, high-level and general-purpose programming language. Python's design philosophy emphasizes code readability with its notable use of significant indentation. Its language constructs and object-oriented approach aim to help programmers write clear, logical code for small and large-scale projects.[29] Python is dynamically-typed and garbage-collected. It supports multiple programming paradigms, including structured (particularly, procedural), object-oriented and functional programming. Python is often described as a batteries included language due to its comprehensive standard library.[30] Guido van Rossum began working on Python in the late 1980's, as a successor to the ABC programming language, and first released it in 1991 as Python 0.9.1.[31] Python 2.0 was released in 2000 and introduced new features, such as list comprehensions and a garbage collection system using reference counting and was discontinued with version 2.7.18 in 2020.[32] Python 3.0 was released in 2008 and was a major revision of the language that is not completely backward-compatible and much Python 2 code does not run unmodified on Python 3. Python consistently ranks as one of the most popular programming languages"
        save_path = 'test_tmp/python.png'
        plot_word_cloud(article, save_path)
        self.assertEqual(os.path.exists(save_path), True)
        os.remove(save_path)
        os.rmdir(folder_dir)
