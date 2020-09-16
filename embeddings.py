from gensim.test.utils import common_texts
from gensim.models.fasttext import FastText
import tweet_analyzer as ta

def get_embeddings_model_from_timeline(timeline):

    corpus = []

    for tweet in timeline:
        corpus.append(ta.extract_keywords_from_tweet(tweet.text, True))
    
    print(corpus)
        

    model = FastText(size=100, window=5, min_count=1)

    model.build_vocab(sentences=corpus)

    model.train(sentences=corpus, total_examples=len(corpus), epochs=10)

    print("Model trained!")

    return model

# Requires a trained model
def get_word_embeddings(model, word: str):
    return model.wv[word]