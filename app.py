from flask import Flask, render_template, url_for, request, redirect
import networkx as nx
import crawler_twitter_api as twitter
import tweet_analyzer as tweet_analyzer
import user_profile_analyzer as user_analyzer
import crawler as c
from threading import Timer

app = Flask(__name__)

crawler = c.Crawler()
test_seeds_videogames = [2394975145, 1269442129, 3153194140, 347831597, 15804774, 1220791675, 2421828871, 1098024347611029504, 18927441, 7157132]

@app.route('/', methods=['POST', 'GET'])
def index():
    return render_template('index.html')

@app.route('/crawler/users/get_id/<name>', methods=['POST', 'GET'])
def get_users_info_by_displayed_name(name):
    users = twitter.get_users_by_names([name])
    return render_template('index.html', users=users)


@app.route('/crawler/users/lookup/<int:list_ids>', methods=['POST', 'GET'])
def get_users_info(list_ids):
    users = twitter.get_users_by_ids([list_ids])
    return render_template('index.html', users=users)

@app.route('/crawler/user/timeline/<int:user_id>', methods=['POST', 'GET'])
def get_users_timeline(user_id):
    statuses = twitter.get_user_timeline_by_id(user_id)
    return render_template('index.html', statuses=statuses)

@app.route('/crawler/user/favorites/<int:user_id>', methods=['POST', 'GET'])
def get_user_recent_favorited_tweets(user_id):
    statuses = twitter.get_recents_favorite_tweets_by_id(user_id)
    return render_template('index.html', statuses=statuses)

@app.route('/crawler/tweet/retweeters/<int:tweet_id>', methods=['POST', 'GET'])
def get_tweet_retweeters(tweet_id):
    users = twitter.get_tweet_retweeted_users(tweet_id)
    return render_template('index.html', users=users)

@app.route('/crawler/user/list/<int:user_id>', methods=['POST', 'GET'])
def get_user_subscriberd_lists(user_id):
    lists = twitter.get_user_subscribed_lists(user_id)
    return render_template('index.html', lists=lists)

@app.route('/crawler/list/subscribers/<int:list_id>', methods=['POST', 'GET'])
def get_list_subscribers(list_id):
    users = twitter.get_list_subscribers(list_id)
    return render_template('index.html', users=users)

@app.route('/crawler/start/', methods=['POST'])
def start_crawling():

        try:
            filterStopwords = False
            predicate = request.form["predicate"]
            # if request.form.get("stopwords") :
            #     filterStopwords = True
            
            stat = Timer(2.0, go_to_crawler_stat)
            crawler.startCrawling(predicate, test_seeds_videogames)
            
            # return render_template('crawler_stat.html', crawler=crawler)
            
            # return render_template('test.html', bioKeywords=keywords)
        except:
            return 'Error on starting crawler'

@app.route('/crawler/get_stat/', methods=['GET'])
def get_crawler_stat():
    return render_template('crawler_stat.html', crawler=crawler)

# Services test
@app.route('/user/bio/test', methods=['GET', 'POST'])
def calculate_user_bio_keywords():
    keywords = []
    if request.method == 'POST':
        try:
            filterStopwords = False
            user_bio = request.form["bio"]
            if request.form.get("stopwords") :
                filterStopwords = True
            keywords = user_analyzer.get_user_bio_keywords(user_bio, filterStopwords)
            return render_template('test.html', bioKeywords=keywords)
        except:
            return 'There was an issue getting the bio'
    else:
        return render_template('test.html', bioKeywords=keywords)


@app.route('/tagme/test', methods=['GET'])
def test_tagme():
    tweet_analyzer.tagme_test()

# SHUTDOWN
def shutdown_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()

@app.route('/shutdown', methods=['GET'])
def shutdown():
    shutdown_server()
    return 'Server shutting down...'

# Support function to crawl start
def go_to_crawler_stat():
    return render_template('crawler_stat.html', crawler=crawler)

@app.route('/crawler/input', methods=['GET'])
def go_to_crawler_input():
     return render_template('crawler_input.html')