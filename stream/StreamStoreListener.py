# Author: Hyeong Joon Suh
# Filename: StreamStoreListener.py
# Description: Class StreamStoreListener that inherits from tweepy.StreamListener.
# Overrides on_status to store streamed tweets into AWS DynamoDB

import tweepy
import boto3
import sys
sys.path.append('../') # hard-coded path to file
from keys.twitter_keys import *
from myNLP.cleanTweets import *

class StreamStoreListener(tweepy.StreamListener):
    def on_status(self, status):
		text = status.text
        #  do not save retweets
		if self.isRetweet(text) or  startsWithMention(text) or containsURL(text):
			return

		# put tweet id and text into aws kinesis
		kinesis = boto3.client("kinesis")
		kinesis.put_record(StreamName="twitter", Data=bytes(status.id_str + " " + text, 'utf-8'), PartitionKey="filler")
        print(status.id_str)

    def on_error(self, status_code):
        # twitter sends 420 when connection rate limited
        if status_code == 420:
            return False
