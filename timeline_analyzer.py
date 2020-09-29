import tweet_analyzer as ta
import crawler as crawler
from boilerpy3 import extractors
import tagme
import crawler_twitter_api as api

coeff_micropost = 1
coeff_cohesiveness = 0
coeff_parents = 1
coeff_siblings = 1

bin_cohesiveness = 0

keywords_interest_treshold = 0.005
goal_treshold = 1


def bin_cohesiveness(cohesiveness):
    if cohesiveness < 0.20:
        return 1
    if cohesiveness <= 0.25:
        return 2
    # value beetween 0.26 and 1
    return 3


estimates_cohesiveness = [0, 33.74, 37.11, 29.15]

'''
    This is called after a timeline is available from a choosen user from Q2 (Timeline Queue)
    Returns: 
    - list of new users
    - if the current user is goal
    - list of goal tweets
'''


def analyze_timeline(timeline, vocabolary, predicate_keywords: list, user_id: int, user_graph, users_goal_ratio: float) -> (bool, list, list):

    is_goal = False
    mentions_users = []
    new_users = []
    retweet_users = []

    ir_post = 0  # Im, interest ratio for micropost's contents
    ir_cohesiveness = 0  # Ia interest_ratio_features

    # Those interest ratio are the topical locality phenoma on the social network
    ir_parents = 0  # If interest_ratio of parents
    ir_siblings_2 = 0  # IF interest_ratio_outdegree

    # 1 Analyze the content interest ratio
    ir_post, goal_tweets, mentions, retweet_users = calculate_content_interest_ratio(
        timeline, vocabolary, predicate_keywords)

    if len(goal_tweets) > 0:
        is_goal = True

    # 2 Calculate the cohesiveness ratio
    binned_cohesiveness = calculate_lexical_cohesion()
    # TODO
    # ir_coh = calculate_cohesiveness_interest_ratio()
    ir_coh = 0

    # 3 Calculate the social tie interest ratio
    ir_parents = calculate_parent_interest_ratio(
        user_id, user_graph, users_goal_ratio)

    ir_siblings = calculate_siblings_interest_ratio(
        user_id, user_graph, users_goal_ratio)

    # 4
    ir_timeline = calculate_timeline_interest_ratio(
        ir_post, ir_coh, ir_parents, ir_siblings)

    print("> Results Timeline (IR: "+ str(ir_timeline) +"): IrPost: "+ str(ir_post)+ " IrCoh: "+ str(ir_coh)+ " IrPar: "+ str(ir_parents)+" IrSib: "+ str(ir_siblings))

    # Frontier Exploring
    if is_goal == True:
        new_users = get_users_from_frontier(user_id, ir_timeline)
        for userId in retweet_users:
            new_users.append((userId, ir_timeline))

    return is_goal, new_users, goal_tweets


'''
    Return interest ratio fro the timeline
    It is also the priority attribute to new user in the
'''


def calculate_timeline_interest_ratio(ir_post, ir_coh, ir_parents, ir_siblings):
    ir_timeline = (coeff_micropost * ir_post) + (coeff_cohesiveness * ir_coh) + (coeff_parents * ir_parents) + (coeff_siblings * ir_siblings)
    return ir_timeline


# Content analysis of microposts
def calculate_content_interest_ratio(timeline, vocabolary, predicate_keywords) -> (float, bool):
    is_goal = False
    goal_tweets = []
    mentions = []
    is_first = True
    interest_ratio_content = 0
    retweeted_users = []

    for tweet in timeline:

        # Find if is goal
        if crawler.predicate_function(tweet.text, predicate_keywords) >= goal_treshold:
            print("*** Found Goal Tweet: "+ str(tweet.id)+" ***")
            is_goal = True
            goal_tweets.append(tweet)
            retweeters = api.get_tweet_retweeted_users(tweet.id)
            for user_id in retweeters:
                retweeted_users.append(user_id)
        
        tweet_ir, tweet_mentions = analyze_tweet(tweet, vocabolary)

        for mention in tweet_mentions:
            mentions.append(mention)

        if is_first == True:
            interest_ratio_content = tweet_ir
        else:
            interest_ratio_content = interest_ratio_content * tweet_ir

    return interest_ratio_content, goal_tweets, mentions, retweeted_users


def analyze_tweet(tweet, vocabolary) -> (float, list):

    keywords = ta.extract_keywords_from_tweet(tweet.text, True)
    interest_ratio_tweet = 0
    is_first = True
    tweet_mentions = ta.get_users_from_tweet(tweet)

    for kw in keywords:
        try:
            kw_interest = vocabolary.keywords[kw]
            if interest > keywords_interest_treshold:
                if is_first == True:
                    interest_ratio_tweet = interest
                    is_first = False
                else:
                    interest_ratio_tweet = interest_ratio_tweet * kw_interest
        except:
            pass

    return interest_ratio_tweet, tweet_mentions


'''
    Based on postulate: "A timeline focused on a limited set of topics has more chances to have 
    ties towards users whose timelines deal with the same topics"
'''


def calculate_lexical_cohesion():

    # TODO: LDA on the recent tweets
    lexical_cohesion = 0

    return bin_cohesiveness(lexical_cohesion)


def calculate_cohesiveness_interest_ratio():
    prEci = estimates_cohesiveness[bin_cohesiveness]
    vci = goal_user_f_bin_i
    vci_negated = total_user_f_bin_i - goal_user_f_bin_i

    ir_cohesiveness = (vci / (prEci * users_goal_ratio)) + (vci_negated / (prEfi * (1 - users_goal_ratio)))
    return ir_cohesiveness

# SOCIAL TIE ANALYSIS

# Returns the siblings of the current user


def get_all_mentioned_users(timeline):
    user_ids = set()
    for tweet in timeline:
        mentions_ids = get_users_from_tweet(tweet)
        for id in mentions_ids:
            user_ids.add(id)
    return user_ids


'''
    .1 if several users that satisfy the predicate mention u, this user has more chances to satisfy the predicate
'''


def calculate_parent_interest_ratio(user_id, user_graph, users_goal_ratio) -> float:

    interest_ratio_parent = 0
    parents = user_graph.get_user_parents(user_id)

    goal_parents = []

    for user in parents:
        if user.is_goal == True:
            goal_parents.append(user)

    # Frequency of: user satisfies the predicate & points to user_id
    try:
        number_goal_parents = len(goal_parents)
        vEpEp = number_goal_parents / len(parents)
        frequency_parents_goal = (
            vEpEp / (users_goal_ratio * users_goal_ratio)) ** number_goal_parents
    except:
        frequency_parents_goal = 0

    # Frequency of: user not satisfies the predicate & point to user_id
    try:
        number_no_goal_parents = len(parents) - len(goal_parents)
        vNotEpEp = number_no_goal_parents / len(parents)
        frequency_parents_no_goal = (
            vNotEpEp / ((users_goal_ratio - 1) * users_goal_ratio)) ** number_no_goal_parents
    except:
        frequency_parents_no_goal = 0

    interest_ratio_parent = frequency_parents_goal + frequency_parents_no_goal

    return interest_ratio_parent


'''
    .2 if u has many siblings that satisfy the predicate, more likely u also satisfy it
'''


def calculate_siblings_interest_ratio(user_id, user_graph, users_goal_ratio) -> float:

    interest_ratio_siblings = 0
    siblings = user_graph.get_user_siblings(user_id)

    goal_siblings = []

    for user in siblings:
        if user.is_goal == True:
            goal_siblings.append(user)

    try:
        interest_ratio_siblings = (
            len(siblings) / (len(goal_siblings) * users_goal_ratio))
    except:
        interest_ratio_siblings = 0
    return interest_ratio_siblings

# EXPLORING THE FRONTIER


def get_users_from_frontier(user_id: int, priority: float) -> list:

    new_users = []
    favorite_users = get_users_from_favorite_tweets(user_id)
    list_users = get_users_from_list(user_id)

    for u_id in favorite_users:
        new_users.append((u_id, priority))
    for u_id in list_users:
        new_users.append((u_id, priority))

    return new_users


def get_users_from_favorite_tweets(user_id: int) -> list:
    favorite_tweets = api.get_recents_favorite_tweets_by_id(user_id)
    users = []
    for tweet in favorite_tweets:
        users.append(tweet.author.id)
    return users


# def get_users_from_retweets(user_id: int) -> list:
#     retweets_tweets = api.get_tweet_retweeted_users(user_id)
#     users = []
#     for tweet in retweets_tweets:
#         users.append(tweet.author)
#     return users

def get_users_from_list(user_id: int) -> list:
    user_lists = api.get_user_subscribed_lists(user_id)
    users = []
    for user_list in user_lists:
        print("Analyzing list: "+ str(user_list.id))
        try:
            subscribers = api.get_list_subscribers(user_list.id)
            for user in subscribers:
                users.append(user.id)
        except:
            pass

    return users