import json
import boto3
import base64

def lambda_handler(event, context):
    if event is None:
        return
    for record in event['Records']:
        data = base64.b64decode(record['kinesis']['data']).decode("utf-8")
        save_data(data)

def save_data(data):
    """
    save data to DynamoDB table
    """
    split = data.split(" ", 1)
    if len(split) != 2:
        return
    id = split[0]
    if not id.isdigit():
        return
    text = split[1]

    dynamodb = boto3.client('dynamodb')
    response = dynamodb.put_item(
            TableName="tweets",
            Item={
                "id" : {"N" : id},
                "text" : {"S": text}
                }
            )

