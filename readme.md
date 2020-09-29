Important! nltk must be downloaded before use:
1. python3
2. import nltk
3. nltk.download()
4. nltk.d => stopwords
5. nltk.download('punkt')

Package dependencies:
- tweepy
- genim (embeddings)
- networkx
- boilerpy3
- tagme
- nltk
- scikitlearn (pip install -U scikit-learn)
- flask (for web app)

# How initialize the project

1. Activate the virtualenv
2. Install all dependencies
3. edit the config_empty.json file. After that, remove the "_empty" from the file name

# How use the crawler

0. Activate the virtualenv (source /../ML_SII_Project/env/bin/activate)

1. Start the "app.py" file by usign the comand "flusk run" and use the webapp functions

2. Run with "python3 crawler.py crawler_input_corona_virus.json"
    (Or with a different valid json)


# TODO:
- Update Cohesiveness bin estimates
- Clean User Bio like tweets
- Function to print user graph
- Better User API usage