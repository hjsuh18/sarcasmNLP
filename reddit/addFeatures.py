import sys
import random
sys.path.append('../') # hard-coded path to file

import boto3
from boto3.dynamodb.conditions import Key, Attr

from py4j.java_gateway import JavaGateway

# retrieve data from DynamoDB table and return as dict
def getData(table_name):
	dynamodb = boto3.resource('dynamodb')
	table = dynamodb.Table(table_name)

	reddit = {}
	response = table.scan()
	data = response['Items']
	for d in data:
		comment_id, parent, sarcastic, text = d["comment_id"], d["parent"], d["sarcastic"], d["text"]
		reddit[comment_id] = (parent, sarcastic, text)
	    
	while response.get('LastEvaluatedKey'):
		response = table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
		data = response['Items']
		for d in data:	
			comment_id, parent, sarcastic, text = d["comment_id"], d["parent"], d["sarcastic"], d["text"]
			reddit[comment_id] = (parent, sarcastic, text)
	return reddit

def uploadData(data, table_name):
	dynamodb = boto3.client('dynamodb')
	count = 0
	for k, v in data.items():
		# change features list format to upload to DynamoDB
		sarcastic, features = v

		formatted_features = []
		for f in features:
			formatted_features.append({"N" : str(f)})

		response = dynamodb.put_item(
			TableName=table_name, 
			Item={
			"id" : {"S" : k}, 
			"sarcastic" : {"BOOL" : sarcastic},
			"features": {"L": formatted_features},
			}
			)
		count = count + 1
		if count % 1000 == 0:
			print(count)

def getFeatures(text, parent, sa):
	features = sa.getFeatures(text)
	positivity = features[0]

	total = 0.0
	count = 0
	for p in parent:
		total = total + sa.getPositivity(p)
		count = count + 1
	if count != 0:
		parentPositivity = total / count
	else:
		parentPositivity = 2.0

	parentChildContrast = round(abs(parentPositivity - positivity), 2)
	features.append(parentPositivity)
	features.append(parentChildContrast)
	return features

def main():
	if len(sys.argv) < 3 or len(sys.argv) > 3:
		print("Invalid number of command-line arguments")

	getDataTableName = sys.argv[1]
	uploadDataTableName = sys.argv[2]

	data = getData(getDataTableName)

	gateway = JavaGateway()
	sa = gateway.entry_point.getSentimentAnalyzer()

	featured_data = {}

	count = 0
	for k, v in data.items():
		parent, sarcastic, text = v
		features = getFeatures(text, parent, sa)
		featured_data[k] = (sarcastic, features)
		count = count + 1
		if count % 1000 == 0:
			print("Features calculated: ", count)

	uploadData(featured_data, uploadDataTableName)

if __name__ == '__main__':
	main()
