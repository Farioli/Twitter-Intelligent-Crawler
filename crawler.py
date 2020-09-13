import crawler_twitter_api as twitter
import user_profile_analyzer as user_analyzer
import crawled_users as cu
import vocabolary as v


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
    vocabolary = v.Vocabolary()

    #Test
    seeds = [(1, 0.87), (1046814112594976768, 0.89), (3, 0.23), (4, 0.25)]

    # INITIALIZZATION
    q2 = []
    q3 = []
    q4 = []
    q5 = []
    q6 = []
    output_tweets = []
    

    # Uf, q1 = frontier users - Each element must be a (user_id, priority)
    frontier = []

    # Uc = Crawled users - Each elements must be: (user_id, goal, keywords, bin_followers, bin_followee)
    crawled_users = cu.CrawledUsers()
    frontier = seeds

    # MAIN LOOP


    #1 - Pop the top user (highest It) from q1 (frontier)
    next_user = get_max_priority_from_queue(frontier)

    user = twitter.get_users_by_ids([next_user[0]])
    
    priority_q2, new_keywords = user_analyzer.analyze_user(user[0], crawled_users, vocabolary)

    q2.append((user, priority_q2))
    
    for key in new_keywords:
        if not key in vocabolary:
            vocabolary.append(key)

    print(vocabolary)
    print(q2)
    

    #2 - Get the Ip from the user profile analysis and push the user in q2

    #3 - Pop the top user in q2 (highest Ip)

    #4 - Analyize the timeline of the q2 user

    #5 - Add user to crawled users (Uc)

    # Update the keywords interest ratio
    vocabolary.update_keywords_interest_ratio(crawled_users)


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


def calculate_cralwer_output(number_of_results):
    return "todo"