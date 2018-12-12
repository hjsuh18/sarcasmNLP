"""
Script to go through all tweets in DynamoDB table and label each entry
as either sarcastic or not sarcastic.
Separate attributes for each different method of labeling.
"""
# import twitter keys and tokens from a separate keys folder
import sys
sys.path.append('../')
from myNLP.labelTweets import hashtagLabel
import boto3

def label(id, text):
	dynamodb = boto3.resource('dynamodb')
	table = dynamodb.Table('tweets')

	isSarcastic = hashtagLabel(text)

	table.update_item(
			Key={
				'id': id,
				},
			UpdateExpression='SET hashtagSarcasm = :val',
			ExpressionAttributeValues={
				':val': isSarcastic
				}
			)
	if isSarcastic:
		print(text)


def main():
	dynamodb = boto3.resource('dynamodb')
	table = dynamodb.Table('tweets')
	response = table.scan()
	count = 0

	data = response['Items']
	for d in data:
		count = count + 1
		if (count % 50) == 0:
			print(count)
		label(d['id'], d['text'])

	while response.get('LastEvaluatedKey'):
		response = table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
		data = response['Items']
		for d in data:
			count = count + 1
			if (count % 50) == 0:
				print(count)
			label(d['id'], d['text'])

if __name__ == "__main__":
	main()

