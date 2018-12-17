# Use searchtweets package to collect tweets with #sarcasm #sarcastic tags

from searchtweets import ResultStream, gen_rule_payload, load_credentials, collect_results
import sys
sys.path.append('../') # hard-coded path to file
from myNLP.cleanTweets import *
from myNLP.labelTweets import *
import boto3
import time

def next_date(date):
    if date == 201811300000:
        return 201812010000
    return date + 10000

TABLE_NAME = "tweets_search"

# Twitter premium load credentials
premium_search_args = load_credentials("../keys/.twitter_keys.yaml",
                                       yaml_key="search_tweets_premium",
                                       env_overwrite=False)

# iterate through different dates
start_date = 201811180000
end_date = 201812160000

while start_date <= end_date:
	# generate valid json queries
	query_rule = gen_rule_payload(
		"#sarcasm lang:en",
		results_per_call=100,
		from_date=str(start_date),
		to_date=str(next_date(start_date))
		)
	#print("Query Rule:")
	#print(query_rule)

	rs = ResultStream(rule_payload=query_rule, max_results=100, **premium_search_args)
	#print(rs)

	tweets = list(rs.stream())

	# get tweets from query and save to dynamodb
	for tweet in tweets:
		text = tweet.all_text
		id = tweet.id
		created_time = tweet.created_at_datetime

		#  do not save retweets
		if isRetweet(text) or  startsWithMention(text) or containsURL(text):
			continue

		text = toLowerCase(text)
		sarcastic = hashtagLabel(text)
		text = removeMention(text)

		print(text)
		print(str(id))
		print(str(created_time))

		dynamodb = boto3.client('dynamodb')
		response = dynamodb.put_item(
			TableName=TABLE_NAME, 
			Item={
			"id" : {"N" : id}, 
			"text" : {"S": text}, 
			"sarcastic": {"BOOL": sarcastic},
			"time": {"S": str(created_time)}
			}
			)
		time.sleep(5)

	start_date = next_date(start_date)
