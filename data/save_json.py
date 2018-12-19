# Parse through comments.json file and upload to DynamoDB
# since the file is too large to process and query in memory.

import ijson
import boto3

f = open('sarc/main/main_comments.json', 'r')

parser = ijson.parse(f)

dynamodb = boto3.client('dynamodb')
TABLE_NAME = "main_comments"

count = 0
# go through json file
for prefix, event, value in parser:
    if event == 'map_key':
        k = value
        v = {}
        # get values for a certain comment key id
        while True:
            prefix, event, value = next(parser)
            if event == 'end_map':
                break
            if event == 'map_key':
                key = value
                prefix, event, value = next(parser)
                v[key] = str(value)

        response = dynamodb.put_item(
            TableName=TABLE_NAME, 
            Item={
            "id" : {"S" : k}, 
            "text" : {"S": v["text"]}, 
            "author": {"S": v["author"]},
            "score": {"N": v["score"]},
            "ups": {"N": v["ups"]},
            "downs": {"N": v["downs"]},
            "date": {"S": v["date"]},
            "created_utc": {"N": v["created_utc"]},
            "subreddit": {"S": v["subreddit"]}
            }
            )

        count = count + 1
        print(str(count) + ": " + k)
