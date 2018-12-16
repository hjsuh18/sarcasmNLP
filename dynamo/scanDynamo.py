# Scan dynamoDB table using boto3

import boto3
from boto3.dynamodb.conditions import Key, Attr

dynamodb = boto3.client('dynamodb')

print("List of tables:")
print(dynamodb.list_tables())

table = dynamodb.Table('tweets')
print("tweets table:")
print(table)

response = table.scan(
        FilterExpression=Attr('sarcastic`').eq(true)
        )
items = response['Items']

print("Number of sarcastic tweets:")
print(len(items))

