class UserData:

    id : int
    is_goal : bool
    keywords : set
    bin_activities: int
    bin_followers : int
    bin_followees : int

    def __init__(self, id, is_goal, keywords, bin_activities, bin_followers, bin_followees):
        self.id = id
        self.is_goal = is_goal
        self.keywords = keywords
        self.bin_activities = bin_activities
        self.bin_followers = bin_followers
        self.bin_followees = bin_followees

    def contains_keyword(self, keyword: str) -> bool:
        return keyword in self.keywords

# Class to handle crawled users
class CrawledUsers:

    # This is a list of all crawled users
    crawled_users : set

    def __init__(self):
        self.crawled_users = set()
    def add_crawled_user(self, user: UserData) -> None:
        self.crawled_users.add(user)

    # Return Ep
    def get_goal_user_ratio(self) -> float:
       return len(crawled_users.get_goal_user_list()) / len(crawled_users.crawled_users)

    # This is used to calculate Ep
    def get_goal_user_list(self) -> set:

        goal_users = set()

        for user in self.crawled_users:
            if user.is_goal == True:
                goal_users.add(user)
        
        return goal_users

    # This is used to calculate Ep AND Pr(wi)
    def get_goal_user_list_by_keyword(self, keyword: str) -> set:

        keyword_goal_users = set()
        goal_users = self.get_goal_user_list()

        for user in goal_users:
            if user.contains_keyword(keyword):
                keyword_goal_users.add(user)
        
        return keyword_goal_users

    # This is used to calculate Pr(wi)
    def get_user_with_keyword(self, keyword: str) -> set:

        keyword_users = set()

        for user in self.crawled_users:
            if user.contains_keyword(keyword):
                keyword_users.add(user)
        
        return keyword_users


    # Returns the user with the bin_i_of_activities
    def get_user_with_bin_i_activities(self, bin:int) -> set:

        bin_activities_user = set()

        for user in self.crawled_users:
            if user.bin_activities == bin:
                bin_activities_user.add(bin_activities_user)
        return bin_activities_user

    # This is used to calculate Va,i (isGoal = True) and !Va,i (isGoal = !True)
    def get_activities_bin_i_user_frequency(self, bin:int, is_goal: bool) -> float:

        activities_total_users = get_user_with_bin_i_activities(bin)
        activities_searched_user = []

        for user in activities_total_users:
            if user.is_goal == is_goal:
                activities_searched_user.add(user)

        return len(activities_searched_user) / len(activities_total_users)

    # TIE STATISTICAL ANALYSIS: Followees    

    # Returns the user with the bin_i_of_followers
    def get_user_with_bin_i_followers(self, bin:int) -> set:

        bin_followers_user = set()

        for user in self.crawled_users:
            if user.bin_followers == bin:
                bin_followers_user.add(bin_followers_user)
        return bin_followers_user

    # This is used to calculate Va,i (isGoal = True) and !Va,i (isGoal = !True)
    def get_followers_bin_i_user_frequency(self, bin:int, is_goal: bool) -> float:

        followers_total_users = get_user_with_bin_i_followers(bin)
        followers_searched_user = []

        for user in followers_total_users:
            if user.is_goal == is_goal:
                followers_searched_user.add(user)

        return len(followers_searched_user) / len(followers_total_users)

    # TIE STATISTICAL ANALYSIS: Followers

    # Returns the user with the bin_i_of_followees
    def get_user_with_bin_i_followees(self, bin:int) -> set:

        bin_followees_user = set()

        for user in self.crawled_users:
            if user.bin_followees == bin:
                bin_followees_user.add(bin_followees_user)
        return bin_followees_user

    # This is used to calculate Va,i (isGoal = True) and !Va,i (isGoal = !True)
    def get_followees_bin_i_user_frequency(self, bin:int, is_goal: bool) -> float:

        followees_total_users = get_user_with_bin_i_followees(bin)
        followees_searched_user = []

        for user in followees_total_users:
            if user.is_goal == is_goal:
                followees_searched_user.add(user)

        return len(followees_searched_user) / len(followees_total_users)