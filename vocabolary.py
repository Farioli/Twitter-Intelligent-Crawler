# This class models the Vk of the crawler, built on the crawled users
class Vocabolary:
    
    # Sets of keywords and relative interest ratios
    keywords : dict
    
    def __init__(self):
        self.keywords = {}

    def add_keyword(self, keyword: str) -> None:
        if not keyword in self.keywords:
            self.keywords[keyword] = 0

    def get_keyword_interest_ratio(keyword :str) -> float:
        ir = 0
        try:
            ir = self.keywords[keyword]
        except:
            ir = 0

        return ir

    def update_keywords_interest_ratio(self, crawled_users) -> None:

        # Pr(Ei)
        goal_ratio = crawled_users.get_goal_user_ratio()

        number_of_users = len(crawled_users.crawled_users)

        for key in self.keywords:
            # Pr(Ep AND wi)
            word_goal_ratio = len(crawled_users.get_goal_user_list_by_keyword(key)) / number_of_users

            #Pr(wi)
            word_ratio = len(crawled_users.get_user_with_keyword(key)) / number_of_users

            interest_keyword = word_goal_ratio / ( goal_ratio * word_ratio )
            self.keywords[key] = interest_keyword