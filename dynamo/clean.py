"""
Script to go through all tweets in DynamoDB table and label each entry
as either sarcastic or not sarcastic.
Separate attributes for each different method of labeling.
"""
# import twitter keys and tokens from a separate keys folder
import sys
sys.path.append('../')
from myNLP.cleanTweets import *
import boto3

def clean(id, text):
	dynamodb = boto3.resource('dynamodb')
	table = dynamodb.Table('tweets')
	if startsWithMention(text) or containsURL(text):
		table.delete_item(Key={'id': id,})
		return
	text = toLowerCase(text)
	text = removeMention(text)
	text = removeHashtag(text)
	table.update_item(
			Key={
				'id': id,
				},
			UpdateExpression='SET text = :val',
			ExpressionAttributeValues={
				':val': text
				}
			)

def main():
	dynamodb = boto3.resource('dynamodb')
	table = dynamodb.Table('tweets')
	response = table.scan()
	count = 0

	data = response['Items']
	for d in data:
		count = count + 1
		clean(d['id'], d['text'])

	while response.get('LastEvaluatedKey'):
		response = table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
		data = response['Items']
		for d in data:
			count = count + 1
			if count % 1000 == 0:
				print(count)
			clean(d['id'], d['text'])

if __name__ == "__main__":
	main()

