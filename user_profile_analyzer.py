import nltk
from dateutil.relativedelta import relativedelta
from datetime import date
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize 

#TODO: must be input
coeff_bio = 1
coeff_features = 1
coeff_indegree = 1
coeff_outdegree = 1

binned_followers = 0
binned_followees = 0

keywords_interest_treshold = 0.005

'''
    Logaritmic Binning for indegree, outdegree and activity coefficient values
'''
def logaritmic_binning(value):
    if value < 10:
        return 1
    if value <= 100:
        return 2
    if value <= 1000:
        return 3
    if value <= 10000:
        return 4
    return 5

# First value is discarded (f = followers, F = followees)
estimated_bin_activities = [0, 27.5, 24.9, 32.4, 13.8, 1.3]
estimates_bin_f = [0, 1.91, 9.31, 33.14, 23.34, 32.40]
estimates_bin_F = [0, 3.67, 13.39, 49.10, 24.22, 9.62]

def get_year_since_creation(creation_date):
    return relativedelta(date.today(), creation_date).years

'''
    user_goal_ratio is the Pr(Ep), the ratio of crawled users that satisfies the predicate
'''
def analyze_user(user, crawled_users, vocabolary):

    ir_bio = 0 # Ib interest_ratio_bio
    ir_act = 0 #Ia interest_ratio_activities
    ir_in = 0 #If interest_ratio_indegree
    ir_out = 0 #IF interest_ratio_outdegree

    # 1 - Calculate bio interest ratio
    bio = user.description
    ir_bio = analyze_bio(bio, crawled_users, vocabolary, True)

    # 2 - Calculate activities interest ratio
    date_creation = user.created_at
    num_post = user.statuses_count
    coeff_activity = num_post / get_year_since_creation(date_creation)
    binned_coeff_activity =  logaritmic_binning(coeff_activity)
    ir_act = analyze_user_activities(binned_activities, crawled_users)

    # 3 - Calculate indegree interest ratio
    binned_followers = logaritmic_binning(user.followers_count)
    ir_in = calculate_user_followers_interest_ratio(binned_followers, crawled_users)

    # 4 - Calculate outdegree interest ratio
    binned_followees = logaritmic_binning(user.friends_count)
    ir_out = alculate_user_followees_interest_ratio(binned_followees, crawled_users)

    # Calculate User Interest Ratio
    user_ir = calculate_user_priority(ir_bio, ir_act, ir_in, ir_out)
    keywords = get_user_bio_keywords(bio, True)

    return (user_ir, keywords)

'''
    Returns the interest ratio for the user bio
'''
def analyze_bio(bio, vocabolary, filterStopwords) -> float:
    
    # Called Sb
    bio_keywords = get_user_bio_keywords(bio, filterStopwords)

    interest_ratio_bio = 0

    bool isFirst = True

    for kw in bio_keywords:
        try:
            kw_interest = vocabolary.keywords[kw]
            if interest > keywords_interest_treshold:
                if isFirst == True:
                    interest_ratio_bio = interest
                    isFirst = False
                else:
                    interest_ratio_bio = interest_ratio_bio * kw_interest
        except:
            pass

    return interest_ratio_bio

''' 
    Returns the interest ratio fro the user activities, Ia
'''
def analyze_user_activities(binned_coeff_activity, crawled_users) -> float:

    prob_activity = estimated_bin_activities[binned_coeff_activity]
    # Event where user satisfies the predicate and has activities in the i activities bin
    prob_act_bin_goal_user = prob_activity * crawled_users.get_goal_user_ratio()
    prob_act_bin_no_goal_user = prob_activity * (1 - crawled_users.get_goal_user_ratio())

    # TODO: si potrebbe fare una cosa più furba
    frequency_user_bin_goal = crawled_users.get_activities_bin_i_user_frequency(binned_coeff_activity, True)
    frequency_user_bin_no_goal = crawled_users.get_activities_bin_i_user_frequency(binned_coeff_activity, False)

    interest_ratio_activities = ( (frequency_user_bin_goal / prob_act_bin_goal_user) + (frequency_user_bin_no_goal / prob_act_bin_no_goal_user) )
    return interest_ratio_activities


'''
    Returns the priority in q2 for the user
'''
def calculate_user_priority(ir_bio: float, ir_act: float, ir_in: float, ir_out: float) -> float:
    ir_profile = [ (ir_bio * coeff_bio) + (ir_act * coeff_features) + (ir_in * coeff_indegree) + (ir_out * coeff_outdegree)]
    return ir_profile

'''
    Goal: valuate the potential correlation beetween 3 class of user
    and the timeline that satisfy the user predicate
    num_followers = fu
    num_followee = Fu
'''
def tie_statistical_analysis(binned_followers, binned_followees):

    # Case where user is news website, radio, television networks, celebrities, politicias, artists
    if binned_followers > binned_followees:
        print("Informations source!")

    if binned_followers == binned_followees:
        print("Reciprocity") 
    
    if binned_followers < binned_followees:
        print("Information seeker...") 
    
'''
    Returns If(Ep)
'''
def calculate_user_followers_interest_ratio(binned_followers:int, crawled_users) -> float:
    prob_followers = estimated_bin_followers[binned_followers]
    goal_users_ratio = crawled_users.get_goal_user_ratio()

    # Event where user satisfies the predicate and has followers in the i followers bin
    prob_followers_bin_goal_user = prob_followers * goal_users_ratio
    prob_followers_bin_no_goal_user = prob_followers * (1 - goal_users_ratio)

    # TODO: si potrebbe fare una cosa più furba
    frequency_user_bin_goal = crawled_users.get_followers_bin_i_user_frequency(binned_followers, True)
    frequency_user_bin_no_goal = crawled_users.get_followers_bin_i_user_frequency(binned_followers, False)

    interest_followers = ( (frequency_user_bin_goal / prob_followers_bin_goal_user) + (frequency_user_bin_no_goal / prob_followers_bin_no_goal_user) )
    return interest_followers

'''
    Returns IF(Ep)
'''
def calculate_user_followees_interest_ratio(followees_number, crawled_users) -> float:

    binned_followers =  logaritmic_binning(followees_number)
    prob_followees = estimated_bin_followees[binned_followees]
    goal_users_ratio = crawled_users.get_goal_user_ratio()

    # Event where user satisfies the predicate and has followees in the i followees bin
    prob_followees_bin_goal_user = prob_followees * goal_users_ratio
    prob_followees_bin_no_goal_user = prob_followees * (1 - goal_users_ratio)

    # TODO: si potrebbe fare una cosa più furba
    frequency_user_bin_goal = crawled_users.get_followees_bin_i_user_frequency(binned_followees, True)
    frequency_user_bin_no_goal = crawled_users.get_followees_bin_i_user_frequency(binned_followees, False)

    interest_followers = ( (frequency_user_bin_goal / prob_followees_bin_goal_user) + (frequency_user_bin_no_goal / prob_followees_bin_no_goal_user) )
    return interest_followers

# UTILITIES FUNCTIONS
def get_user_bio_keywords(bio, filterStopwords):
    bio_keywords = set()
    bio = bio.replace(",", " ")
    bio = bio.replace(".", " ")
    bio_keywords = bio.split(" ")

    if filterStopwords == True :
        print("Filtering stopwords...")
        # Delete stopwords from bio
        stop_words = stopwords.words('english')
        word_tokens = word_tokenize(bio) 
        filtered_sentence = set()

        for w in word_tokens: 
            if w not in stop_words: 
                filtered_sentence.add(w) 
        bio_keywords = filtered_sentence
    return bio_keywords