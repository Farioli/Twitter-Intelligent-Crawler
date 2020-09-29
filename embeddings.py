from gensim.test.utils import common_texts, get_tmpfile
from gensim.models.fasttext import FastText

# https://radimrehurek.com/gensim/auto_examples/howtos/run_downloader_api.html
import gensim.downloader as api

import numpy as np

import tweet_analyzer as ta

def download_embeddings_model():

    print("> Downloading the embeddings model")
    model = api.load('glove-twitter-25')
    print("> Embeddings model downloaded!")
    return model

# Old version with timeline as corpus
def get_embeddings_model_from_timeline(timeline):

    corpus = []
    
    # for tweet in timeline:
    #     corpus.append(ta.extract_keywords_from_tweet(tweet.text, True))
    
    print(corpus)
        
    model = FastText(size=10, window=5, min_count=1)

    model.build_vocab(sentences=corpus)

    model.train(sentences=corpus, total_examples=len(corpus), epochs=10)

    print("Model trained!")

    return model

# Requires a trained model
def get_word_embeddings(model, word: str):
    return model.wv[word]

def get_timeline_embeddings_sum(timeline, model):
    
    is_first = True
    sum_vector = np.array([0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0])

    for tweet in timeline:
        keywords = ta.extract_keywords_from_tweet(tweet.text, True)
        for kw in keywords:
            try:
                keyword_embs = get_word_embeddings(model, kw)
            except:
                keyword_embs = np.array([0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0])
            if is_first is True:
                sum_vector = keyword_embs
                is_first = False
            else:
                sum_vector = np.add(sum_vector, keyword_embs)
    return sum_vector  