# Parse through comments.json file and upload to DynamoDB
# since the file is too large to process and query in memory.
import csv
import boto3
from boto3.dynamodb.conditions import Key, Attr

# return text value of key in main_comments table
def query_main_comments(key):
    dynamodb = boto3.client('dynamodb')
    response = dynamodb.query(
        TableName="main_comments",
        KeyConditionExpression='id = :comment_id',
        ExpressionAttributeValues={':comment_id': {"S" : key}}
        )
    items = response['Items']
    if not items:
        return None
    return items[0]['text']['S']

def upload_csv(csvfile, table_name):
    dynamodb = boto3.client('dynamodb')

    f = open(csvfile, 'rt')
    csv_reader = csv.reader(f)

    for row in csv_reader:
        parents, comments, labels = row[0].split('|')

        # get parent comments from dynamodb
        parents = parents.split()
        parent_posts = []
        for i in range(0, len(parents)):
            text = query_main_comments(parents[i])
            if text:
                parent_posts.append({"S" : text})

        # get comments from dynamodb
        comments = comments.split()

        # 1 : sarcastic, 0: not sarcastic
        labels = labels.split()

        # put in a new entry for each comment-label pair
        for i in range(0, len(comments)):
            text = query_main_comments(comments[i])
            if not text:
                continue

            sarcastic = labels[i] == '1'

            # put this information into DynamoDB table
            response = dynamodb.put_item(
                TableName=table_name, 
                Item={
                "comment_id" : {"S" : comments[i]}, 
                "text" : {"S": text}, 
                "sarcastic" : {"BOOL" : sarcastic},
                "parent" : {"L" : parent_posts}
                }
                )

CSV1 = "sarc/main/test-balanced.csv"
CSV2 = "sarc/main/test-unbalanced.csv"
CSV3 = "sarc/main/train-balanced.csv"
CSV4 = "sarc/main/train-unbalanced.csv"

TABLE1 = "reddit_test_balanced"
TABLE2 = "reddit_test_unbalanced"
TABLE3 = "reddit_train_balanced"
TABLE4 = "reddit_train_unbalanced"

upload_csv(CSV1, TABLE1)
upload_csv(CSV2, TABLE2)
upload_csv(CSV3, TABLE3)
upload_csv(CSV4, TABLE4)
