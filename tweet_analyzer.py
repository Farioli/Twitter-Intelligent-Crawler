# TagMe references: https://pypi.org/project/tagme/
import tagme

# Boilerpy3 references: https://pypi.org/project/boilerpy3/
import boilerpy3

import json


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

# TEST
def tagme_test():
    lunch_annotations = tagme.annotate("My favourite meal is Mexican burritos.")

    # Print annotations with a score higher than 0.1
    for ann in lunch_annotations.get_annotations(0.1):
        print(ann)
