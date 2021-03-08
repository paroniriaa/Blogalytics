import os
import json
from collections import Counter

import nltk
from nltk import word_tokenize
from nltk.stem import PorterStemmer

from tqdm import tqdm
import numpy as np
import matplotlib.pyplot as plt
import torch

from fairseq.models.bart import BARTModel


bart = BARTModel.from_pretrained(
    'checkpoints/',
    checkpoint_file='checkpoint1.pt',
    data_name_or_path='data/bin'
)

bart.cuda()
bart.eval()
bart.half()

def inference_batch(batch, min_len=10):
    assert type(batch) == list
    assert type(batch[0]) == str
    with torch.no_grad():
        pred = bart.sample(batch, beam=1, lenpen=2.0, max_len_b=140, min_len=min_len, no_repeat_ngram_size=3)
    return pred
