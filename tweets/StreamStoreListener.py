# Author: Hyeong Joon Suh
# Filename: StreamStoreListener.py
# Description: Class StreamStoreListener that inherits from tweepy.StreamListener.
# Overrides on_status to store streamed tweets into AWS DynamoDB

import tweepy

class StreamStoreListener(tweepy.StreamListener):
	def on_status(self, status):
		# need to change to store into DynamoDB
		print(status.text)