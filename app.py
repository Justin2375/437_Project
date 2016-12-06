#!flask/bin/python
import tweepy
from flask import Flask,render_template
import sys
from textblob import TextBlob
from credentials import secret

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('sentiment.html', name = 'Ayush' )
def calculateSentiment():
    cons_key = secret['cons_key']
    sec_cons_key = secret['sec_cons_key']
    accs_token = secret['accs_token']
    sec_accs_token = secret['sec_accs_token']
    tweetsList = []
    authenticate = tweepy.OAuthHandler(cons_key, sec_cons_key)
    authenticate.set_access_token(accs_token, sec_accs_token)

    twitter = tweepy.API(authenticate)

    tweets = twitter.search('trump')

    for tweet in tweets:
     #   print(tweet.text)
        sentiment = TextBlob(tweet.text)
      #  print(sentiment.sentiment.polarity)
        tweetsList.append((tweet.text, sentiment.sentiment.polarity))
    return tweetsList
if __name__ == '__main__':
    print(calculateSentiment())
    app.run(debug=True)