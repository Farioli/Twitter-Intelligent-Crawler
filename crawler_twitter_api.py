# Tweepy api reference: http://docs.tweepy.org/en/latest/api.html

import tweepy
import json

with open("config.json") as json_data_file:
    config = json.load(json_data_file)

consumer_key = config["twitter"]["consumer_key"]
consumer_secret = config["twitter"]["consumer_secret"]
access_token = config["twitter"]["access_token"]
access_token_secret = config["twitter"]["access_token_secret"]

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

# public_tweets = api.home_timeline()
# for tweet in public_tweets:
#     print(tweet.text)


# USER PROFILE
'''
    #1 users/lookup
    @user_ids must be a list of ids
    Output: List of Users
'''
def get_users_by_ids(user_ids):
    users_info = api.lookup_users(user_ids=user_ids)
    print(users_info)
    return users_info

'''
    #2 statuses/user_timeline
    Output: List of Statuses (tweets)
'''
def get_user_timeline_by_id(user_id):
    timeline = api.user_timeline(id=user_id)
    print(timeline)
    return timeline

# WEAK TIES

'''
    #3 favorites/list
    Returns a list of intergs, that are the users who have 
    retweeted the tweet specified by id
    Output: list of Status objs
'''
def get_recents_favorite_tweets_by_id(user_id):
    favorited_tweets = api.favorites(id=user_id)
    print(favorited_tweets)
    return favorited_tweets

'''
    #4 statuses/retweeters/ids
    Returns a list of intergs, that are the users who have 
    retweeted the tweet specified by id
    Output: list of User objs
'''
def get_tweet_retweeted_users(tweet_id):
    user_ids_list = api.retweeters(tweet_id)
    print(user_ids_list)
    return user_ids_list

'''
    #5 lists/list
    Output: list of List objs
'''
def get_user_subscribed_lists(user_id):
    user_lists = api.lists_all(user_id=user_id)
    print(user_lists)
    return user_lists

'''
    #6 lists/subscribers
    Output: List of User objs
'''
def get_list_subscribers(list_id):
    subscribers = api.list_subscribers(list_id=list_id)
    print(subscribers)
    return subscribers

# SEARCH

'''
    Search with queries of max 500 characters
    Output: SearchResults Object
'''
def search_query_in_tweets(query):
    results = None
    if len(query)<= 500 : 
        results = api.search(q=query)
    return results





# print(get_user_timeline_by_id('nicolebun6'))
#print(get_recents_favorite_tweets_by_id(config["test_id"]))