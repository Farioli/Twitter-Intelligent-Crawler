import tweet_analyzer as ta
import crawler as crawler
from boilerpy3 import extractors
import tagme

coeff_micropost = 1
coeff_cohesiveness = 0
coeff_siblings = 1
coeff_siblings_2 = 1

bin_cohesiveness = 0

keywords_interest_treshold = 0.005
goal_treshold = 1

def bin_cohesiveness(cohesiveness):
    if value < 0.20:
        return 1
    if value <= 0.25:
        return 2
    # value beetween 0.26 and 1
    return 3

estimates_cohesiveness = [0, 33.74, 37.11, 29.15]

'''
    This is called after a timeline is available from a choosen user from q2
'''
def analyze_timeline(timeline, vocabolary, predicate):

    is_goal = False

    ir_micropost = 0 # Ib interest_ratio_bio
    ir_cohesiveness = 0 #Ia interest_ratio_features

    # Those interest ratio are the topical locality phenoma on the social network
    ir_siblings = 0 #If interest_ratio_indegree
    ir_siblings_2 = 0 #IF interest_ratio_outdegree

    # 1 Analyze the content interest ratio
    #TODO
    ir_micropost, goal_tweets = calculate_content_interest_ratio(timeline, vocabolary)

    # 2 Calculate the binning for this timeline
    binned_cohesiveness = calculate_lexical_cohesion()
    ir_cohesiveness = calculate_cohesiveness_interest_ratio()

    #3 Calculate the social tie interest ratio
    #TODO



    return calculate_timeline_interest_ratio()

'''
    Return interest ratio fro the timeline
    It is also the priority attribute to new user in the
'''
def calculate_timeline_interest_ratio():
    ir_timeline = [(coeff_micropost * ir_micropost) + (coeff_cohesiveness * ir_cohesiveness) + (coeff_siblings * ir_siblings) + (coeff_siblings_2 * ir_siblings_2)]
    return ir_timeline


# Content analysis of microposts
def calculate_content_interest_ratio(timeline, vocabolary, predicate) -> (float, bool):
    is_goal = False
    goal_tweets = []
    is_first = True
    interest_ratio_content = 0

    for tweet in timeline:
        
        # Find if is goal
        if crawler.predicate_function(tweet, predicate) >= goal_treshold:
            is_goal = True
            goal_tweets.add(tweet)
        tweet_ir = analyze_tweet(tweet, vocabolary)
        if is_first = True:
            interest_ratio_content = tweet_ir
        else:
            interest_ratio_content = interest_ratio_content * tweet_ir
    
    return interest_ratio_content


def analyze_tweet(tweet, vocabolary) -> (float):

    keywords = ta.extract_keywords_from_tweet(tweet.text)
    interest_ratio_tweet = 0
    is_first = True

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

    return interest_ratio_tweet


'''
    Based on postulate: "A timeline focused on a limited set of topics has more chances to have 
    ties towards users whose timelines deal with the same topics"
'''
def calculate_lexical_cohesion():

    #TODO: LDA on the recent tweets
    lexical_cohesion = 0

    return bin_cohesiveness(lexical_cohesion)

def calculate_cohesiveness_interest_ratio():
    prEci = estimates_cohesiveness(bin_cohesiveness)
    vci = goal_user_f_bin_i
    vci_negated = total_user_f_bin_i - goal_user_f_bin_i

    ir_cohesiveness = [ (vci / (prEci * users_goal_ratio)) + (vci_negated / ( prEfi * (1 - users_goal_ratio))) ]
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
def 

'''
    .2 if u has many siblings that satisfy the predicate, more likely u also satisfy it
'''