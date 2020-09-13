import crawler as crawler
import crawled_users as cu

# crawled_users_example = [
#     (1, False, ['palla', 'gino', 'spettacolo', 'casa'], 1, 3),
#     (2, True, ['sedia', 'cioè', 'palla', 'boh'], 3, 4),
#     (3, True, ['finalmente', 'gino', 'spettacolo', 'casa'], 2, 5),
#     (4, False, ['palla', 'nave', 'vento', 'pioggia'], 5, 3),
#     (5, False, ['sole', 'carlo', 'sera', 'finalmente'], 3, 3),
# ]

user1 = cu.UserData(1, False, {'palla', 'gino', 'spettacolo', 'casa'},1, 1, 3)
user2 = cu.UserData(2, True, {'sedia', 'cioè', 'palla', 'boh'},2, 3, 4)
user3 = cu.UserData(3, True, {'finalmente', 'gino', 'spettacolo', 'casa'},2, 2, 5)
user4 = cu.UserData(4, False, {'palla', 'nave', 'vento', 'pioggia'},3, 5, 3)
user5 = cu.UserData(5, False, {'sole', 'carlo', 'sera', 'finalmente'},5, 3, 3)

crawled_users = cu.CrawledUsers()

crawled_users.add_crawled_user(user1)
crawled_users.add_crawled_user(user2)
crawled_users.add_crawled_user(user3)
crawled_users.add_crawled_user(user4)
crawled_users.add_crawled_user(user5)


def test_crawling():
    crawler.crawling("Yu-Gi-Oh", [(1, 0.87), (1046814112594976768, 0.89), (3, 0.23), (4, 0.25)])

def test_get_frontier_best_user():
    frontier = [(1, 0.87), (2, 0.89), (3, 0.23), (4, 0.25)]
    result = crawler.get_max_priority_from_queue(frontier)
    print(result == (2, 0.89))

def test_get_goal_user():
    print(len(crawled_users.get_goal_user_list()) == 2)

def test_get_goal_user_by_keywords():
    sedia_goal = crawler.get_goal_user_list_by_keyword(crawled_users_example, "sedia")
    palla_goal = crawler.get_goal_user_list_by_keyword(crawled_users_example, "palla")
    sole_goal = crawler.get_goal_user_list_by_keyword(crawled_users_example, "sole")
    print(len(sedia_goal) == 1)
    print(len(palla_goal) == 1)
    print(len(sole_goal) == 0)


test_get_goal_user()