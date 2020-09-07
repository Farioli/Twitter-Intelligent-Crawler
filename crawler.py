import crawler_twitter_api as twitter


predicate_keywords = []
vocabolary = []

# interesting user / total user analyzed
prEp = 1

# Uc
crawled_users = []

# Uf
frontier_users = []


q1 = []
q2 = []
q3 = []
q4 = []
q5 = []
q6 = []

retrieved_tweets = []

output_tweets = []

def init_crawler(seeds):
    q1 = []
    q2 = []
    q3 = []
    q4 = []
    q5 = []
    q6 = []
    crawled_users = []
    frontier_users = seeds

'''
    Seeds is a list of twitter user ids
'''
def crawling(predicate, seeds):

    init_crawler(seeds)
    q1 = seeds
    tweets = []

    #1 - Pop the top user (highest It) from q1 (frontier)

    #2 - Get the Ip from the user profile analysis and push the user in q2

    #3 - Pop the top user in q2 (highest Ip)

    #4 - Analyize the timeline of the q2 user

    #5 - Add user to crawled users (Uc)


    return tweets
    #todo

'''
    ft : T -> {0,1}
    Returns 1 if the tweet satisfies the user's predicate
'''
def predicate_function(tweet, predicate):
    #TODO: search predicate in tweet and tweet contents
    results = 0

    return results

'''
    fu : User -> {0,1}
    1 if the timeline of the user has at least one tweet that satisfies the predicate function
'''
def user_function(user_id, predicate):

    found = False
    timeline = twitter.get_user_timeline_by_id(user_id)

    for(tweet in timeline):
        if predicate_function(tweet, predicate) == 1:
            found = True
    return found


def calculate_output(number_of_results):
    return "todo"