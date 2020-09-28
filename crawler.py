import crawler_twitter_api as twitter
import user_profile_analyzer as user_analyzer
import crawled_users as cu
import vocabolary as v
import timeline_analyzer as timeline
import tweet_analyzer as ta
import threading
import user_graph as g
import time
import sys
import json

# interesting user / total user analyzed
prEp = 1

q2 = []

retrieved_tweets = []
output_tweets = []
timeout = False


def onTimeout():
    timeout = True


'''
    Seeds is a list of twitter user ids
'''


def crawling(predicate: str, seeds: list, max_time: float):

    timeout = False
    timer = threading.Timer(max_time, onTimeout)

    predicate_keywords = []
    vocabolary = v.Vocabolary()
    graph = g.UserGraph()

    # Uf, q1 = frontier users - Each element must be a (user_id, priority)
    frontier = []

    # Test
    for el in seeds:
        frontier.append((el, 0))

    # INITIALIZZATION
    q2 = []
    output_tweets = []

    # Uc = Crawled users - Each elements must be: (user_id, goal, keywords, bin_followers, bin_followee)
    crawled_users = cu.CrawledUsers()

    # MAIN LOOP

    while(timeout == False):

        # 1 - Pop the top user (highest It) from q1 (frontier)
        next_user = get_max_priority_from_queue(frontier)

        user_data = twitter.get_users_by_ids([next_user[0]])

        # 2 - Get the Ip from the user profile analysis and push the user in q2
        priority_q2, new_crawl_user = user_analyzer.analyze_user(
            user_data[0], crawled_users, vocabolary)

        q2.append((new_crawl_user, priority_q2))

        for key in new_crawl_user.keywords:
            vocabolary.add_keyword(key)

        # Update the keywords interest ratio
        vocabolary.update_keywords_interest_ratio(crawled_users)

        print(vocabolary)
        print(q2)

        # 3 - Pop the top user in q2 (highest Ip)
        next_user_for_timeline = get_max_priority_from_queue(q2)
        q2_user = next_user_for_timeline[0]

        # 4 - Analyize the timeline of the q2 user
        user_timeline = twitter.get_user_timeline_by_id(q2_user.id)

        is_goal, new_users, goal_tweets = timeline.analyze_timeline(
            user_timeline, vocabolary, predicate_keywords, q2_user.id, graph, crawled_users.get_goal_user_ratio())

        for u in new_users:
            frontier.append(new_users)

        for t in goal_tweets:
            output_tweets.append(t)

        # 5 - Add user to crawled users (Uc)
        q2_user.is_goal = is_goal
        crawled_users.add_crawled_user(q2_user)
        graph.add_user(q2_user)
        timout = True

        print(frontier)
        print(q2)

    # return tweets
    print(output_tweets)


'''
    ft : T -> {0,1}
    Returns 1 if the tweet satisfies the user's predicate
'''


def predicate_function(tweet_text: str, predicate_keywords: list):
    # TODO: search predicate in tweet and tweet contents
    results = 0

    keywords = ta.extract_keywords_from_tweet(tweet_text, True)

    for key in keywords:
        if key.lower() in predicate_keywords:
            results = 1
            break

    return results


'''
    fu : User -> {0,1}
    1 if the timeline of the user has at least one tweet that satisfies the predicate function
'''


def user_function(user_id, predicate):

    found = False
    timeline = twitter.get_user_timeline_by_id(user_id)

    for tweet in timeline:
        if predicate_function(tweet.text, predicate) == 1:
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


class Crawler:
    predicate_keywords = []
    frontier = []
    timeline_queue = []
    vocabolary = v.Vocabolary()
    # Uc = Crawled users - Each elements must be: (user_id, goal, keywords, bin_followers, bin_followee)
    crawled_users = cu.CrawledUsers()
    graph = g.UserGraph()
    output_tweets = []
    deleted_users = []
    start_timer = 0
    is_crawling = False

    def __init__(self):
        self.predicate_keywords = []
        self.frontier = []
        self.timeline_queue = []
        self.vocabolary = v.Vocabolary()
        # Uc = Crawled users - Each elements must be: (user_id, goal, keywords, bin_followers, bin_followee)
        self.crawled_users = cu.CrawledUsers()
        self.graph = g.UserGraph()
        self.output_tweets = []
        self.deleted_users = []
        self.start_time = 0
        self.total_seconds_crawling = 0
        self.is_crawling = False

    def startCrawling(self, predicate, seeds, total_seconds_crawling: int):

        # Start Timer
        self.is_crawling = True
        self.start_time = time.time()
        self.total_seconds_crawling = total_seconds_crawling

        self.timeout = False
        # timer = threading.Timer(max_time, onTimeout)

        temp_predicate = predicate.split(" ")
        for w in temp_predicate:
            self.predicate_keywords.append(w.lower())

        print("PREDICATE KEYWORDS" + str(len(self.predicate_keywords)))

        for keyword in self.predicate_keywords:
            print("Keyword:" + str(keyword))

        self.vocabolary = v.Vocabolary()
        self.graph = g.UserGraph()

        # Uf, q1 = frontier users - Each element must be a (user_id, priority)
        self.frontier = []

        # Test
        for el in seeds:
            self.frontier.append((el, 0))

        # INITIALIZZATION
        self.timeline_queue = []
        self.output_tweets = []

        # Uc = Crawled users - Each elements must be: (user_id, goal, keywords, bin_followers, bin_followee)
        self.crawled_users = cu.CrawledUsers()

        # MAIN LOOP
        while self.is_time_remained():

            print("=== New Crawler Step ===")

            if len(self.frontier) > 0:
                # 1 - Pop the top user (highest It) from q1 (frontier)
                next_user = get_max_priority_from_queue(self.frontier)
                try:
                    print("Analyzing user with id:" + str(next_user[0]))
                    
                    user_data = twitter.get_users_by_ids([next_user[0]])

                    # 2 - Get the Ip from the user profile analysis and push the user in timeline_queue
                    priority_q2, new_crawl_user = user_analyzer.analyze_user(
                        user_data[0], self.crawled_users, self.vocabolary)

                    print("Adding " + str(new_crawl_user.id) + "with priority "+ str(priority_q2) +" to q2")

                    self.timeline_queue.append((new_crawl_user, priority_q2))

                    for key in new_crawl_user.keywords:
                        self.vocabolary.add_keyword(key)
                except:
                    self.deleted_users.append(
                        (next_user, e.__class__))
                    pass

            if len(self.timeline_queue) > 0:
                # 3 - Pop the top user in q2 (highest Ip)
                next_user_for_timeline = get_max_priority_from_queue(
                    self.timeline_queue)
                try:
                    q2_user = next_user_for_timeline[0]

                    print("Analyzing user: "+ str(q2_user.id))

                    # 4 - Analyize the timeline of the q2 user
                    user_timeline = twitter.get_user_timeline_by_id(q2_user.id)

                    is_goal, new_users, goal_tweets = timeline.analyze_timeline(
                        user_timeline, self.vocabolary, self.predicate_keywords, q2_user.id, self.graph, self.crawled_users.get_goal_user_ratio())

                    for u in new_users:
                        self.frontier.append(new_users)

                    for t in goal_tweets:
                        self.output_tweets.append(t)

                    # 5 - Add user to crawled users (Uc)
                    q2_user.is_goal = is_goal
                    self.crawled_users.add_crawled_user(q2_user)

                    # Update the keywords interest ratio
                    self.vocabolary.update_keywords_interest_ratio(
                        self.crawled_users)
                    
                    self.graph.add_user(q2_user)
                    
                except Exception as e:
                    self.deleted_users.append(
                        (next_user_for_timeline, e.__class__))
                    print("Error on extracting user from q2")

            print("End of one crawler step.\n")
            print("Remaining in frontier: "+ str(len(self.frontier)) +"\n")
            print("Remaining in timeline queue: "+ str(len(self.timeline_queue)) +"\n")
            print("==================================================================")

        self.is_crawling = False

        # return tweets
        print("Output tweets:" + output_tweets)

    def get_elapsed_time(self):
        now = time.time()
        return now - self.start_time

    def is_time_remained(self) -> bool:
        return (self.total_seconds_crawling - self.get_elapsed_time()) > 0

    def stop_crawl(self):
        self.timeout = True

    def get_crawled_user_length(self):
        return len(self.crawled_users.crawled_users)

    def get_frontier_length(self):
        return len(self.frontier)

    def get_timeline_queue_length(self):
        return len(self.timeline_queue)

    def get_deleted_users_length(self):
        return len(self.deleted_users)


def main():
    if len(sys.argv) != 2:
        print("Insert the parameters json, please")
        return

    #parse the parameters json input
    try:
        with open(sys.argv[1]) as parameters_json:
            parameters_dict = json.load(parameters_json)
            predicate = parameters_dict["predicate"]
            seeds = parameters_dict["seeds"]
            total_seconds = parameters_dict["crawlingSeconds"]
    except:
        print("Error taking the parameters from json")
        return
    
    crawler = Crawler()

    try:
        print("Starting")
        crawler.startCrawling(predicate, seeds, total_seconds)
    except:
        print("Error starting the crawler")

if __name__ == "__main__":
    main()