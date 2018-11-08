# Author: Hyeong Joon Suh
# Filename: stream_tweets.py
# Description: Streams tweets using tweepy package

import tweepy
from StreamStoreListener import StreamStoreListener

# import twitter keys and tokens from a separate keys folder
import sys
sys.path.append('../keys') # hard-coded path to file
from twitter_keys import *

def main():
	# OAuth authentication to access Twitter API
	auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_token, access_secret)
	api = tweepy.API(auth)

	streamStoreListener = StreamStoreListener()
	stream = tweepy.Stream(auth = api.auth, listener=streamStoreListener)

	stream.filter(track=['Trump'])

if __name__ == '__main__':
	main()