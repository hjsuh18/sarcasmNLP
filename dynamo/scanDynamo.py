# Scan dynamoDB table using boto3

import boto3
from boto3.dynamodb.conditions import Key, Attr

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('tweets')
print("tweets table item count:")
print(table.item_count)

print("Number of sarcastic tweets:")
count = 0

response = table.scan(
        FilterExpression=Attr('sarcastic').eq('true')
        )
data = response['Items']
for d in data:
	count = count + 1
	print(count)

while response.get('LastEvaluatedKey'):
	print("New Batch")
	response = table.scan(
		FilterExpression=Attr('sarcastic').eq(True),
		ExclusiveStartKey=response['LastEvaluatedKey']
		)
	data = response['Items']
	for d in data:
		count = count + 1
		print(count)

print("Final Count:")
print(count)