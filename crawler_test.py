import crawler as crawler
import crawled_users as cu
import user_profile_analyzer as upa
import tweet_analyzer as ta
import vocabolary as v
import crawler_twitter_api as api
import user_graph as g
import embeddings as embs
import numpy as np

test_user_id = 1098024347611029504

test_seeds_videogames = [2394975145, 1269442129, 3153194140, 347831597,
                         15804774, 1220791675, 2421828871, 1098024347611029504, 18927441, 7157132]

user1 = cu.UserData(1, False, {'palla', 'gino', 'spettacolo', 'casa'}, 1, 1, 3, 0)
user2 = cu.UserData(2, True, {'sedia', 'cioè', 'palla', 'boh'}, 2, 3, 4, 1)
user3 = cu.UserData(
    3, True, {'finalmente', 'gino', 'spettacolo', 'casa'}, 2, 2, 5, 0)
user4 = cu.UserData(4, False, {'palla', 'nave', 'vento', 'pioggia'}, 3, 5, 0, 1)
user5 = cu.UserData(5, False, {'sole', 'carlo', 'sera', 'finalmente'}, 5, 3, 1, 0)

crawled_users = cu.CrawledUsers()

crawled_users.add_crawled_user(user1)
crawled_users.add_crawled_user(user2)
crawled_users.add_crawled_user(user3)
crawled_users.add_crawled_user(user4)
crawled_users.add_crawled_user(user5)

vocabolary = v.Vocabolary()

timeline = api.get_user_timeline_by_id(test_user_id)

graph = g.UserGraph()


def test_crawling():
    crawler.crawling("Videogames", test_seeds_videogames, 600)


def test_get_frontier_best_user():
    frontier = [(1, 0.87), (2, 0.89), (3, 0.23), (4, 0.25)]
    result = crawler.get_max_priority_from_queue(frontier)
    print(result == (2, 0.89))


def test_get_goal_user():
    print(len(crawled_users.get_goal_user_list()) == 2)


def test_get_goal_user_by_keywords():
    sedia_goal = crawler.get_goal_user_list_by_keyword(
        crawled_users_example, "sedia")
    palla_goal = crawler.get_goal_user_list_by_keyword(
        crawled_users_example, "palla")
    sole_goal = crawler.get_goal_user_list_by_keyword(
        crawled_users_example, "sole")
    print(len(sedia_goal) == 1)
    print(len(palla_goal) == 1)
    print(len(sole_goal) == 0)

# TEST


def tagme_test():
    lunch_annotations = tagme.annotate(
        "My favourite meal is Mexican burritos.")

    # Print annotations with a score higher than 0.1
    for ann in lunch_annotations.get_annotations(0.1):
        print(ann)


def test_tweet_analyzer():
    tweet = timeline[0]
    keywords = ta.extract_keywords_from_tweet(tweet.text, True)
    print(keywords)

# Test Graph


def test_graph():
    graph.add_user(user1)
    print(graph.get_user(user1.id))

# Test Embeddings


def test_embeddings():
    model = embs.get_embeddings_model_from_timeline(timeline)
    print(embs.get_word_embeddings(model, "catch"))

def test_embeddings_by_dowloaded_corpus():
    model = embs.download_embeddings_model()
    embeddings = embs.get_word_embeddings(model, "catch")
    print("embeddings_1")
    print(embeddings)
    embeddings_2 = embs.get_word_embeddings(model, "try")
    print("embeddings_2")
    print(embeddings_2)
    embs_sum = np.add(embeddings, embeddings_2)  
    print(embs_sum)

def test_timeline_embeddings():
    model = embs.download_embeddings_model()
    embeddings_sum = embs.get_timeline_embeddings_sum(timeline, model)
    print(embeddings_sum)

def test_get_timeline_cohesiveness(user_id):
    model = embs.download_embeddings_model()
    test_timeline = api.get_user_timeline_by_id(user_id)
    embeddings_sum = embs.get_timeline_embeddings_sum(test_timeline, model)
    lexical_cohesion = np.linalg.norm(embeddings_sum)
    print("Cohesiveness of timeline: "+ str(lexical_cohesion))

# Test Crawler Goal

def test_twitter_goal():
    predicate_keywords = ['thanks']
    tweet_text = 'Thanks for watching!\n\nTomorrow will be the Korean #T7OpenChallenge Exhibitions featuring:\n\n1)@eyemusician_TK vs…'
    result = crawler.predicate_function(tweet_text, predicate_keywords)


def test_timeline_goal(id, keyword):
    timeline = api.get_user_timeline_by_id(id)
    result = False
    predicate_keywords = [keyword]
    for tweet in timeline:
        if crawler.predicate_function(tweet.text, predicate_keywords):
            result = True 

    print(result)

def test_list_user_extraction():
    user_id = 2914144864
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


# test_timeline_goal(974693992318324736, 'beer')
# est_list_user_extraction()

print("More general")

print("Washington post")
test_get_timeline_cohesiveness(2467791)

print("CNN")
test_get_timeline_cohesiveness(428333)

print("More specific")

print("Food review")
test_get_timeline_cohesiveness(14476971)

print("League of legends")
test_get_timeline_cohesiveness(577401044)