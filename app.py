from flask import Flask, render_template, url_for, request, redirect
import crawler_twitter_api as twitter

app = Flask(__name__)

@app.route('/', methods=['POST', 'GET'])
def index():
    return render_template('index.html')

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