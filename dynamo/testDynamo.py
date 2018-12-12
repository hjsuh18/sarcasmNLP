import boto3

dynamodb = boto3.client('dynamodb')
print(dynamodb.list_tables())
response = dynamodb.put_item(
        TableName="tweets",
        Item={
            "id" : {"N" : "12345"},
            "text" : {"S" : "trump sucks"}
            }
        )
