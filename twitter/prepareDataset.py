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

# returns a tuple of length 2
# first element is subset of d of size num
# second element is rest of d
def splitDict(d, num):
	sample1 = {}
	sample2 = {}
	randomSample = random.sample(range(1, len(d)), num)
	counter = 0
	for k, v in d.items():
		counter = counter + 1
		if counter in randomSample:
			sample1[k] = v	
		else:
			sample2[k] = v
	return (sample1, sample2)

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
	return round(total / len(l), 2)

def uploadData(data, table_name):
	gateway = JavaGateway()
	sa = gateway.entry_point.getSentimentAnalyzer()

	ep = EmojiParse()

	dynamodb = boto3.client('dynamodb')

	for k, v in data.items():
		text, emoji, sentiment = ep.emoji_parse(k)

		sarcastic = v[0]
		id = v[1]

		emojiSentiment = emoji_sentiment_average(sentiment)
		positivity, adjacentContrast, maxPhrase, minPhrase, phraseContrast = sa.getFeatures(text)
		emojiSentenceContrast = round(abs(emojiSentiment - positivity), 2)

		features = []
		features.append({"N" : str(positivity)})	
		features.append({"N" : str(adjacentContrast)})
		features.append({"N" : str(maxPhrase)})
		features.append({"N" : str(minPhrase)})
		features.append({"N" : str(phraseContrast)})
		features.append({"N" : str(emojiSentiment)})
		features.append({"N" : str(emojiSentenceContrast)})

		response = dynamodb.put_item(
			TableName=table_name, 
			Item={
			"id" : {"N" : str(id)}, 
			"sarcastic" : {"BOOL" : sarcastic},
			"text" : {"S": text}, 
			"features": {"L": features},
			}
			)

def main():
	tweets_search = getData("tweets_search")
	tweets_stream = getData("tweets_sarcastic")
	sarcastic = mergeDicts(tweets_search, tweets_stream)
	# strangely doesn't give exactly 1209 tweets
	non_sarcastic = getRandomSample("tweets_hashtag", 1230)
	non_sarcastic = splitDict(non_sarcastic, 1209)[0]

	if len(sarcastic) != len(non_sarcastic):
		print("Error: data is not balanced")
		return

	print("sarcastic tweet count: ", len(sarcastic))	
	print("non_sarcastic tweet count: ", len(non_sarcastic))

	# split into training and testing datasets
	sarcastic_test, sarcastic_train = splitDict(sarcastic, len(sarcastic) // 5)
	non_sarcastic_test, non_sarcastic_train = splitDict(non_sarcastic, len(non_sarcastic) // 5)

	test = mergeDicts(sarcastic_test, non_sarcastic_test)
	train = mergeDicts(sarcastic_train, non_sarcastic_train)

	uploadData(test, "twitter_test")
	uploadData(train, "twitter_train")

if __name__ == '__main__':
	main()
