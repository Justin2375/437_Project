import tweepy
import sys
from textblob import TextBlob
from credentials import secret

cons_key = secret['cons_key']
sec_cons_key = secret['sec_cons_key']
accs_token = secret['accs_token']
sec_accs_token = secret['sec_accs_token']

authenticate = tweepy.OAuthHandler(cons_key, sec_cons_key)
authenticate.set_access_token(accs_token, sec_accs_token)

twitter = tweepy.API(authenticate)

args = sys.argv

tweets = twitter.search(args[1])

for tweet in tweets:
    print(tweet.text)
    sentiment = TextBlob(tweet.text)
    print(sentiment.sentiment.polarity)
