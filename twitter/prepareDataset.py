import sys
import random
sys.path.append('../') # hard-coded path to file
from myNLP.cleanTweets import *
from myNLP.EmojiParse import EmojiParse

import boto3
from boto3.dynamodb.conditions import Key, Attr

from py4j.java_gateway import JavaGateway


# cleans tweet by using methods from myNLP.cleanTweets
def cleanTweet(tweet):
	tweet = replaceAmp(tweet)
	tweet = removeLTGT(tweet)
	tweet = removeHashtagSarcasm(tweet)
	tweet = removeHashtag(tweet)
	return tweet

# retrieve data from DynamoDB table
# remove twitter '&amp' and '#' from hashtags
def getData(table_name):
	dynamodb = boto3.resource('dynamodb')
	table = dynamodb.Table(table_name)

	tweets = {}
	response = table.scan()
	data = response['Items']
	for d in data:
	    text, sarcastic, id = d["text"], d["sarcastic"], d["id"]
	    text = cleanTweet(text)
	    if text not in tweets and sarcastic:
	        tweets[text] = (sarcastic, id)
	    
	while response.get('LastEvaluatedKey'):
		response = table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
		data = response['Items']
		for d in data:
			text, sarcastic, id = d["text"], d["sarcastic"], d["id"]
			text = cleanTweet(text)
			if text not in tweets and sarcastic:
				tweets[text] = (sarcastic, id)
	return tweets

# get random sample of n items from dynamodb table table_name
def getRandomSample(table_name, n):	
	sample = {}
	dynamodb = boto3.resource('dynamodb')
	table = dynamodb.Table(table_name)
	total = table.item_count

	randomSample = random.sample(range(1, total), n)

	counter = 0

	response = table.scan()
	data = response['Items']

	for d in data:
		counter = counter + 1
		if counter not in randomSample:
			continue
		text, sarcastic, id = d["text"], d["sarcastic"], d["id"]

	    # in tweets_hashtag table, there are fewer than 10 sarcastic tweets
	    # out of over a million
		if sarcastic:
			print("You are incredibly unlucky")

		text = cleanTweet(text)
		sample[text] = (sarcastic, id)

	while response.get('LastEvaluatedKey'):
		response = table.scan(
			ExclusiveStartKey=response['LastEvaluatedKey']
			)
		data = response['Items']
		for d in data:
			counter = counter + 1
			if counter not in randomSample:
				continue
			text, sarcastic, id = d["text"], d["sarcastic"], d["id"]
			
			# in tweets_hashtag table, there are fewer than 10 sarcastic tweets
			# out of over a million
			if sarcastic:	
				print("You are incredibly unlucky")

			text = cleanTweet(text)
			sample[text] = (sarcastic, id)

	return sample

def mergeDicts(d1, d2):
	merged = {}
	for k, v in d1.items():
		merged[k] = v
	for k, v in d2.items():
		if k not in merged:
			merged[k] = v
	return merged

# return average of list, 2.0 (neutral) if l is empty
def emoji_sentiment_average(l):
	if len(l) == 0:
		return 2.0
	total = 0.0
	for x in l:
		total = total + x
	return total / len(l)

def main():
	tweets_search = getData("tweets_search")
	tweets_stream = getData("tweets_sarcastic")
	tweets = mergeDicts(tweets_search, tweets_stream)
	# strangely doesn't give exactly 1209 tweets
	# got around problem in jupyter notebook by getting a larger sample
	# and then removing a few entries
	sample = getRandomSample("tweets_hashtag", 1209)
	tweets = mergeDicts(tweets, sample)
	print(len(tweets))

	gateway = JavaGateway()
	sa = gateway.entry_point.getSentimentAnalyzer()

	ep = EmojiParse()

	dynamodb = boto3.client('dynamodb')

	for k, v in tweets.items():
		text, emoji, sentiment = ep.emoji_parse(k)

		sarcastic = v[0]
		id = v[1]

		emojiSentiment = emoji_sentiment_average(sentiment)
		positivity, adjacentContrast, maxPhrase, minPhrase, phraseContrast = sa.getFeatures(text)
		emojiSentenceContrast = emojiSentiment - positivity

		features = []
		features.append({"N" : positivity})	
		features.append({"N" : adjacentContrast})
		features.append({"N" : maxPhrase})
		features.append({"N" : minPhrase})
		features.append({"N" : phraseContrast})
		features.append({"N" : emojiSentiment})
		features.append({"N" : emojiSentenceContrast})

		response = dynamodb.put_item(
			TableName="twitter_dataset", 
			Item={
			"id" : {"N" : id}, 
			"sarcastic" : {"BOOL" : sarcastic},
			"text" : {"S": text}, 
			"features": {"L": features},
			}
			)

if __name__ == '__main__':
	main()
