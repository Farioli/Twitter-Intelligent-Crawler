import crawler_twitter_api as twitter




# interesting user / total user analyzed
prEp = 1


q2 = []
q3 = []
q4 = []
q5 = []
q6 = []

retrieved_tweets = []

output_tweets = []

'''
    Seeds is a list of twitter user ids
'''
def crawling(predicate, seeds):

    predicate_keywords = []
    vocabolary = []

    #Test
    seeds = [(1, 0.87), (2, 0.89), (3, 0.23), (4, 0.25)]

    # INITIALIZZATION
    q2 = []
    q3 = []
    q4 = []
    q5 = []
    q6 = []

    crawled_users = []
    output_tweets = []
    

    # Uf, q1 = frontier users - Each element must be a (user_id, priority)
    frontier = []

    # Uc = Crawled users - Each elements must be: (user_id, goal, keywords, bin_followers, bin_followee)
    crawled_users = []
    frontier = seeds

    # MAIN LOOP


    #1 - Pop the top user (highest It) from q1 (frontier)
    next_user_id = get_max_priority_from_queue(frontier)
    print(frontier)

    #2 - Get the Ip from the user profile analysis and push the user in q2

    #3 - Pop the top user in q2 (highest Ip)

    #4 - Analyize the timeline of the q2 user

    #5 - Add user to crawled users (Uc)


    # return tweets

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

    for tweet in timeline:
        if predicate_function(tweet, predicate) == 1:
            found = True
    return found

# utility: get the user with max priority
def get_max_priority_from_queue(user_queue):

    if len(user_queue) > 0:
        max_priority_user = user_queue[0]
        for user in user_queue:
            if user[1] > max_priority_user[1]:
                max_priority_user = user
        user_queue.remove(max_priority_user)
        return max_priority_user
    else:
        return "Empty!"

# This is used to calculate Ep
def get_goal_user_list(crawled_users):

    goal_users = []

    for user in crawled_users:
        if user[1] == True:
            goal_users.append(user)
    
    return goal_users

# This is used to calculate Pr(wi)
def get_goal_user_list_by_keyword(crawled_users, keyword):

    keyword_goal_users = []

    for user in crawled_users:
        if user[1] == True:
            if keyword in user[2]:
                keyword_goal_users.append(user)
    
    return keyword_goal_users


def calculate_cralwer_output(number_of_results):
    return "todo"