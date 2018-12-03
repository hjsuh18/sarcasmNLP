# Author: Hyeong Joon Suh
# Filename: StreamStoreListener.py
# Description: Class StreamStoreListener that inherits from tweepy.StreamListener.
# Overrides on_status to store streamed tweets into AWS DynamoDB

import tweepy
import boto3
import sys
sys.path.append('../keys') # hard-coded path to file
from twitter_keys import *

class StreamStoreListener(tweepy.StreamListener):
    def is_retweet(self, text):
        """
        text : str
            text of tweet
        returns boolean, true if tweet is retweet
        """
        if 'RT @' in text:
            return True
        else:
            return False

    def on_status(self, status):
        #  do not save retweets
        if self.is_retweet(status.text):
            return
        # put tweet id and text into aws kinesis
        kinesis = boto3.client("kinesis")
        kinesis.put_record(StreamName="twitter", Data=bytes(status.id_str + " " + status.text, 'utf-8'), PartitionKey="filler")
        print(status.id_str)

    def on_error(self, status_code):
        # twitter sends 420 when connection rate limited
        if status_code == 420:
            return False
