import sys
import random
sys.path.append('../') # hard-coded path to file

import boto3
from boto3.dynamodb.conditions import Key, Attr

from py4j.java_gateway import JavaGateway

# retrieve data from DynamoDB table and return as dict
# lo and hi denote the boundaries of indexes to get from table
def getData(table_name, lo, hi):
	dynamodb = boto3.resource('dynamodb')
	table = dynamodb.Table(table_name)

	counter = -1

	reddit = {}
	response = table.scan()
	data = response['Items']
	for d in data:
		counter = counter + 1
		if counter < lo or counter >= hi:
			continue
		comment_id, parent, sarcastic, text = d["comment_id"], d["parent"], d["sarcastic"], d["text"]
		reddit[comment_id] = (parent, sarcastic, text)
	    
	while response.get('LastEvaluatedKey'):
		response = table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
		data = response['Items']
		for d in data:	
			counter = counter + 1
			if counter < lo or counter >= hi:
				continue
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
# list[0]: whole sentence positivity score
# list[1]: adjacent sentiment contrast score 	
# list[2]: maximum phrase sentiment score
# list[3]: minimum phrase sentiment score
# list[4]: phrase sentiment contrast score
# list[5]: positivity score of parent
# list[6]: parent-child sentiment contrast
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
	if len(sys.argv) != 3 and len(sys.argv) != 5:
		print("Invalid number of command-line arguments")

	getDataTableName = sys.argv[1]
	uploadDataTableName = sys.argv[2]

	data = {}	
	lo = 0
	hi = sys.maxsize
	if len(sys.argv) == 5:
		lo = int(sys.argv[3])
		hi = int(sys.argv[4])

	data = getData(getDataTableName, lo, hi)

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
