import nltk
from dateutil.relativedelta import relativedelta
from datetime import date
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize 

ir_bio = 0 # Ib interest_ratio_bio
ir_features = 0 #Ia interest_ratio_features
ir_indegree = 0 #If interest_ratio_indegree
ir_outdegree = 0 #IF interest_ratio_outdegree

coeff_bio = 1
coeff_features = 1
coeff_indegree = 1
coeff_outdegree = 1

binned_followers = 0
binned_followees = 0

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
estimates_bin_f = [0, 1.91, 9.31, 33.14, 23.34, 32.40]
estimates_bin_F = [0, 3.67, 13.39, 49.10, 24.22, 9.62]

def get_year_since_creation(creation_date):
    return relativedelta(date.today(), creation_date).years

'''
    user_goal_ratio is the Pr(Ep), the ratio of crawled users that satisfies the predicate
'''
def analyze_user(user, users_goal_ratio):

    bio = user.description
    date_creation = user.created_at
    num_post = user.statuses_count
    num_followers = user.followers_count
    num_followees =  user.friends_count

    binned_followers = logaritmic_binning(num_followees)
    binned_followees = logaritmic_binning(num_followers)

    coeff_activity = num_post / get_year_since_creation(date_creation) 

    ir_bio = analyze_bio(bio, True)
    ir_features = 0

    ir_indegree = 0
    ir_outegree = 0

    user_ir = calculate_user_priority()
    keywords = get_user_bio_keywords(bio, True)

    return (user_ir, keywords)

'''
    Returns the interest ratio for the user bio
'''
def analyze_bio(bio, filterStopwords):
    
    # Called Sb
    bio_keywords = []

    interest_ratio_bio = 1

    for keyword in bio_keywords:
        print("TODO")

    interest_ratio_bio = 0

    return interest_ratio_bio

'''
    Returns the priority in q2 for the user
'''
def calculate_user_priority():
    ir_profile = [ (ir_bio * coeff_bio) + (ir_features * coeff_features) + (ir_indegree * coeff_indegree) + (ir_outdegree * coeff_outdegree)]
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
def calculate_user_followers_interest_ratio(goal_user_f_bin_i, total_user_f_bin_i):

    prEfi = estimates_bin_f(binned_followers)
    vfi = goal_user_f_bin_i
    vfi_negated = total_user_f_bin_i - goal_user_f_bin_i

    interest_f = [ (vfi / (prEfi * users_goal_ratio)) + (vfi_negated / ( prEfi * (1 - users_goal_ratio))) ]
    return intereset_f

'''
    Returns IF(Ep)
'''
def calculate_user_followees_interest_ratio(goal_user_F_bin_i, total_user_F_bin_i):

    prEFi = estimates_bin_f(binned_followees)
    vFi = goal_user_F_bin_i
    vFi_negated = total_user_F_bin_i - goal_user_F_bin_i

    interest_f = [ (vFi / (prEFi * users_goal_ratio)) + (vFi_negated / ( prEFi * (1 - users_goal_ratio))) ]
    return intereset_f

# UTILITIES FUNCTIONS
def get_user_bio_keywords(bio, filterStopwords):
    bio_keywords = []
    bio = bio.replace(",", " ")
    bio = bio.replace(".", " ")
    bio_keywords = bio.split(" ")

    if filterStopwords == True :
        print("Filtering stopwords...")
        # Delete stopwords from bio
        stop_words = stopwords.words('english')
        word_tokens = word_tokenize(bio) 
        filtered_sentence = []

        for w in word_tokens: 
            if w not in stop_words: 
                filtered_sentence.append(w) 
        bio_keywords = filtered_sentence
    return bio_keywords