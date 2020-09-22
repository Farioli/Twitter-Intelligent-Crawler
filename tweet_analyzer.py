# TagMe references: https://pypi.org/project/tagme/
import tagme

# Boilerpy3 references: https://pypi.org/project/boilerpy3/
from boilerpy3 import extractors
import json
import re
import string

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
    mentions = tweet.entities
    # print("Mentions" + str(mentions))

    for mention in mentions["user_mentions"]:
        user_ids.append(mention["id"])
    return user_ids

# Get the keywords of the text


def extract_keywords_from_tweet(text: str, filterStopwords: bool) -> set:

    extractor = extractors.ArticleExtractor()
    keywords = set()
    # print(text)
    links = get_urls_from_text(text)
    # print("Debug: number of links:"+ str(len(links)))

    # From disaster dataset
    text = clean_text(text)

    keywords = text.split(" ")

    for key in keywords:
        if key in string.punctuation:
            keywords.remove(key)

    if filterStopwords == True:
        # print("Filtering stopwords...")
        # Delete stopwords from text
        stop_words = stopwords.words('english')
        word_tokens = word_tokenize(text)
        filtered_sentence = set()

        for w in word_tokens:
            if w not in stop_words:
                filtered_sentence.add(w)
        keywords = filtered_sentence

    for url in links:
        # print("Url" + str(url))
        try:
            external_content = extractor.get_content_from_url(url)
            annotations = tagme.annotate(external_content)
            for ann in annotations.get_annotations(annotation_score_treshold):
                print(ann)
                keywords.add(ann.entity_title)
        except:
            pass

    return keywords

# Returns the list of url contained in a text


def get_urls_from_text(text: str) -> list:
    regex = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"
    url = re.findall(regex, text)
    return [x[0] for x in url]

# TEXT CLEANING FUNCTIONS (from: https://www.kaggle.com/odessing/disaster-tweets/data)
# Removes url in the text


def remove_URL(text):
    url = re.compile(r'https?://\S+|www\.\S+')
    return url.sub(r'', text)

# Removes HTML code


def remove_html(text):
    html = re.compile(r'<.*?>')
    return html.sub(r'', text)

# Removes emoji from text


def remove_emoji(text):
    emoji_pattern = re.compile("["
                               u"\U0001F600-\U0001F64F"  # emoticons
                               u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                               u"\U0001F680-\U0001F6FF"  # transport & map symbols
                               u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                               u"\U00002702-\U000027B0"
                               u"\U000024C2-\U0001F251"
                               "]+", flags=re.UNICODE)
    return emoji_pattern.sub(r'', text)

# combines the above 3 functions


def clean_text(text):
    text = remove_URL(text)
    text = remove_html(text)
    text = remove_emoji(text)
    return text

# Tweets are written fast with lots of spelling errors. the function belows does some basic spell checking.
# Hopefully we can now categorize misspelled and correctly spelled words together.
# Spellchecking slightly improves model performance
# spell = SpellChecker(distance=1) # distance=2 is standard but very slow

# def correct_spelling(text):
#     corrected_text = []
#     misspelled_words = spell.unknown(text.split())
#     for word in text.split():
#         if word in misspelled_words:
#             corrected_text.append(spell.correction(word))
#         else:
#             corrected_text.append(word)
#     return " ".join(corrected_text)
