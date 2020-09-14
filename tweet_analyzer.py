# TagMe references: https://pypi.org/project/tagme/
import tagme

# Boilerpy3 references: https://pypi.org/project/boilerpy3/
from boilerpy3 import extractors
import json
import re

import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize 

annotation_score_treshold = 0.1


with open("config.json") as json_data_file:
    config = json.load(json_data_file)

# Set the authorization token for subsequent calls.
tagme.GCUBE_TOKEN = config["tagme_token"]


def does_tweet_contains_user(tweet, user):
    user_ids = get_users_from_tweet(tweet)
    if user.id in user_ids:
        return True
    else:
        return False

# Get the ids of the tweet's mentioned users
def get_users_from_tweet(tweet):
    user_ids = []
    for mention in tweet["entities"]["user_mentions"]:
        user_ids.append(mention["id"])
    return user_ids

# Get the keywords of the text
def extract_keywords_from_tweet(text: str, filterStopwords: bool) -> set:

    extractor = extractors.ArticleExtractor()

    keywords = set()
    links = get_urls_from_text(text)
    print("Debug: number of links:"+ str(len(links)))
    
    # # Clean from http
    # for key in keywords:
    #     if key in links:
    #         keywords.remove(key)
    for url in links:
        text = text.replace(url, "")

    text = text.replace(",", " ")
    keywords = text.split(" ")


    if filterStopwords == True :
        print("Filtering stopwords...")
        # Delete stopwords from text
        stop_words = stopwords.words('english')
        word_tokens = word_tokenize(text) 
        filtered_sentence = set()

        for w in word_tokens: 
            if w not in stop_words: 
                filtered_sentence.add(w) 
        keywords = filtered_sentence

    
    
    for url in links:
        print("Url" + str(url))
        try:
            external_content = extractor.get_content_from_url(url)
            print(external_content)
            annotations = tagme.annotate(external_content)
            for ann in annotations.get_annotations(annotation_score_treshold):
                keywords.add(ann)
        except:
            pass

    return keywords

# Returns the list of url contained in a text
def get_urls_from_text(text:str) -> list:
    regex = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"
    url = re.findall(regex, text)       
    return [x[0] for x in url] 


