#!flask/bin/python
import tweepy
from flask import Flask,render_template,request
import sys
from textblob import TextBlob
from credentials import secret
import pygal
from pygal.style import DarkSolarizedStyle
dist={}

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('sentiment.html')

def find_sent(sentiments):
    dist = {'Positive': 0,'Neutral': 0, 'Negative': 0, 'Average':0.0}

    for i in sentiments:
        #print(i[1])
        dist['Average'] += i[1]
        if (i[1] < -0.2):
            dist['Negative'] += 1
        elif (i[1] > 0.2):
            dist['Positive'] += 1
        else:
            dist['Neutral'] += 1

    dist['Average'] /= len(sentiments)


    print (dist)
    return dist

@app.route('/', methods=['POST'])
def index_post():

    text = request.form['topic']
    sentiments = calculateSentiment(text)
    print(sentiments)


    distribution = find_sent(sentiments)
    print (distribution.values())
    sentis = distribution.values()
    senti_labels =  distribution.keys()
    #global dist = dist
    print (dist)
    # create a bar chart
    bar_chart = pygal.Bar(width=1200, height=600,
                          explicit_size=True,
                          style=DarkSolarizedStyle,
                          disable_xml_declaration=True)
    bar_chart.x_labels = senti_labels
    bar_chart.add('Sentiments', sentis)
    return render_template('sentimentResults.html', tweets = sentiments, sentiment = distribution,bar_chart=bar_chart)
@app.route('/image')
def generate_chart():
    sentis = [1,2,3]
    senti_labels = ['P','Nue','N']
    #global dist = dist
    print (dist)
    # create a bar chart
    bar_chart = pygal.Bar(width=1200, height=600,
                          explicit_size=True,
                          style=DarkSolarizedStyle,
                          disable_xml_declaration=True)
    bar_chart.x_labels = senti_labels
    bar_chart.add('Sentiments', sentis)
    return render_template('chart.html',
                           bar_chart=bar_chart)

def calculateSentiment(topic):
    cons_key = secret['cons_key']
    sec_cons_key = secret['sec_cons_key']
    accs_token = secret['accs_token']
    sec_accs_token = secret['sec_accs_token']
    tweetsList = []
    authenticate = tweepy.OAuthHandler(cons_key, sec_cons_key)
    authenticate.set_access_token(accs_token, sec_accs_token)

    twitter = tweepy.API(authenticate)

    #topic = request.form['text']

    tweets = twitter.search(topic)

    for tweet in tweets:
     #   print(tweet.text)
        sentiment = TextBlob(tweet.text)
      #  print(sentiment.sentiment.polarity)
        tweetsList.append((tweet.text,sentiment.sentiment.polarity))
    return tweetsList

#@app.route("/simple.png")
#def simple():



if __name__ == '__main__':
    #print(calculateSentiment())
    app.run(debug=True)
