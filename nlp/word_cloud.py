import os

import numpy as np
import matplotlib.pyplot as plt

from wordcloud import WordCloud
from nltk.tokenize import word_tokenize


with open('nlp/data/stopwords.txt', 'r') as file:
    lines = file.readlines()
    _stopwords = [line.strip('\n') for line in lines]

def remove_stop_words(article):
    word_tokens = word_tokenize(article.lower())
    filtered_tokens = []
    for w in word_tokens:
        if w not in _stopwords:
            if w not in ',.!?':
                filtered_tokens.append(w)
    return filtered_tokens

def plot_word_cloud(artcile, target_path='figs/cloud.png'):
    tokens = remove_stop_words(artcile)
    tokens = ' '.join(tokens)
    wordcloud = WordCloud(width=1600,
                          height=800,
                          background_color="white").generate(tokens)
    plt.figure(figsize=(20, 10))
    plt.imshow(wordcloud)
    plt.axis("off")
    plt.tight_layout(pad=0)
    plt.savefig(target_path, bbox_inches='tight', dpi=500)
    # plt.show()

# plot_word_cloud('This article is a sample article.')
