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
    try:
        users_info = api.lookup_users(user_ids=user_ids)
        #print(users_info)
        return users_info
    except Exception as e:
        print("Error on getUsers at: "+ str(user_ids[0]))
        print(e)
        


'''
    #2 users/lookup
    @user_ids must be a list of string
    Output: List of Users
'''
def get_users_by_names(user_names):
    try:
        users_info = api.lookup_users(screen_names=user_names)
        #print(users_info)
        return users_info
    except Exception as e:
        print("Error on getUsersByName at: "+ str(user_names[0]))
        print(e)

'''
    #2 statuses/user_timeline
    Output: List of Statuses (tweets)
'''
def get_user_timeline_by_id(user_id):
    try:
        timeline = api.user_timeline(id=user_id)
        # Debug print(timeline)
        return timeline
    except Exception as e:
        print("Error on getTimeline of: "+ str(user_id))
        print(e)


# WEAK TIES

'''
    #3 favorites/list
    Returns a list of intergs, that are the users who have 
    retweeted the tweet specified by id
    Output: list of Status objs
'''
def get_recents_favorite_tweets_by_id(user_id):
    try:
        favorited_tweets = api.favorites(id=user_id)
        # print(favorited_tweets)
        return favorited_tweets
    except Exception as e:
        print("Error on getFavorites of: "+ str(user_id))
        print(e)
        return []

'''
    #4 statuses/retweeters/ids
    Returns a list of intergs, that are the users who have 
    retweeted the tweet specified by id
    Output: list of User objs
'''
def get_tweet_retweeted_users(tweet_id):
    try:
        user_ids_list = api.retweeters(tweet_id)
        # print(user_ids_list)
        return user_ids_list
    except Exception as e:
        print("Error on getRetweeted of: "+ str(tweet_id))
        print(e)
        return []

'''
    #5 lists/list
    Output: list of List objs
'''
def get_user_subscribed_lists(user_id):
    try:
        user_lists = api.lists_all(user_id=user_id)
        # print(user_lists)
        return user_lists
    except Exception as e:
        print("Error on get subscribed list of user: "+ str(user_id))
        print(e)
        return []

'''
    #6 lists/subscribers
    Output: List of User objs
'''
def get_list_subscribers(list_id):
    try:
        subscribers = api.list_subscribers(list_id=list_id)
        # print(subscribers)
        return subscribers
    except Exception as e:
        print("Error on get list subscribers of list: "+ str(list_id))
        print(e)
        return []

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