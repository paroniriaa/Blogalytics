import os

import numpy as np
import matplotlib.pyplot as plt

from wordcloud import WordCloud
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize



nltk.download('stopwords')

def remove_stop_words(article):
    stop_words = set(stopwords.words('english'))
    word_tokens = word_tokenize(article)
    filtered_tokens = []
    for w in word_tokens:
        if w not in stop_words:
            if w not in ',.!?':
                filtered_tokens.append(w)
    return filtered_tokens

def plot_word_cloud(artcile, target_path='figs/cloud.png'):
    tokens = remove_stop_words(artcile)
    x, y = np.ogrid[:300, :300]
    mask = (x - 150) ** 2 + (y - 150) ** 2 > 130 ** 2
    mask = 255 * mask.astype(int)

    wc = WordCloud(background_color="white", repeat=True, mask=mask)
    wc.generate(' '.join(tokens))
    plt.axis("off")
    plt.imshow(wc, interpolation="bilinear")
    # plt.show()
    plt.savefig(target_path, bbox_inches='tight', dpi=500)

# plot_word_cloud('This article is a sample article.')
