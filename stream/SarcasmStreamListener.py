# Author: Hyeong Joon Suh
# Filename: StreamStoreListener.py
# Description: Class StreamStoreListener that inherits from tweepy.StreamListener.
# Overrides on_status to store streamed tweets into AWS DynamoDB
# Use Python 2.7 - 3.6 when using tweepy
import tweepy
import boto3
import sys
sys.path.append('../') # hard-coded path to file
from keys.twitter_keys import *
from myNLP.cleanTweets import *

class SarcasmStreamListener(tweepy.StreamListener):
    def on_status(self, status):
        text = status.text
        #  do not save retweets
        if isRetweet(text) or  startsWithMention(text) or containsURL(text):
            return

        print(status.id_str)
        print(text)

    def on_error(self, status_code):
        # twitter sends 420 when connection rate limited
        if status_code == 420:
            return False
