from dateutil.relativedelta import relativedelta
from datetime import date

ir_bio = 0 # Ib interest_ratio_bio
ir_features = 0 #Ia interest_ratio_features
ir_indegree = 0 #If interest_ratio_indegree
ir_outdegree = 0 #IF interest_ratio_outdegree

coeff_bio = 1
coeff_features = 1
coeff_indegree = 1
coeff_outdegree = 1

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

def get_year_since_creation(creation_date):
    return relativedelta(date.today(), creation_date).years

'''

'''
def analyze_user(user):

    bio = user["description"]
    date_creation = user["created_at"]
    num_post = user["statuses_count"]
    num_followers = ["followers_count"]
    num_followees =  user["friends_count"]

    coeff_activity = num_post / get_year_since_creation(date_creation) 

    ir_bio = analyze_bio(bio)
    ir_features = 0

    ir_indegree = 0
    ir_indegree = 0

    return calculate_user_priority()

'''

'''
def analyze_bio(bio):

    #TODO: eliminare stopwords dalla bio
    # Sb
    bio_keywords = []

    interest_ratio_bio = 1

    for keyword in bio_keywords:

    interest_ratio_bio = 0

    return interest_ratio_bio

'''
    Returns the priority for the user in the q2
'''
def calculate_user_priority():
    ir_profile = [ (ir_bio * coeff_bio) + (ir_features * coeff_features) + (ir_indegree * coeff_indegree) + (ir_outdegree * coeff_outdegree)]
    return ir_profile

