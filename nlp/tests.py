from django.test import TestCase

from nlp.tfidf import *
from nlp.word_cloud import *


class BuildIdvVocabTests(TestCase):

    def test_build_idf_vocab(self):
        out_dict = build_idf_vocab(corpus=['hi world', 'hi mick'])
        self.assertEqual(out_dict['hi'], 0.0)
        self.assertEqual(out_dict['world'], out_dict['mick'])

    def test_get_tf_vocab(self):
        _ = get_tf_vocab("Hello world this is an article for testing")


    def test_get_tf_vocab(self):
        tf_vocab = {'a': 0.1, 'b': 0.3, 'c': 0.5}
        idf_vocab = {'a': 0.1, 'b': 2.0, 'd': 1.0}
        out = get_tfidf_score(tf_vocab, idf_vocab)
        self.assertEqual(out[0][0], 'b')
        self.assertEqual(out[1][0], 'a')
        self.assertEqual(out[2][0], 'c')
        self.assertEqual(out[2][1], 0)

    def test_set_idf_vocab_from_pkl(self):
        _ = setup_idf_vocab()

    def test_set_idf_vocab_from_corpus(self):
        path = 'nlp/data/fake_file.pkl'
        _ = setup_idf_vocab(
        idf_vocab_pkl_path=path)
        os.remove(path)


class WordCloudTests(TestCase):

    def test_remove_stop_words(self):
        article = 'i am a stop words, but book is not'
        filtered_tokens = remove_stop_words(article)
        # only non-stops words are 'stop', 'words', 'book'
        self.assertEqual(len(filtered_tokens), 3)
