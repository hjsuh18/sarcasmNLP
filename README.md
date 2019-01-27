# sarcasmNLP
Class project to train a machine learning model to detect sarcasm on Twitter and Reddit.

## Modules
* consume
	* Amazon kclpy to consume data from AWS Kinesis stream
	* `python consume/consumer.py` to start consuming data
* corenlp
	* Stanford CoreNLP module to use Socher et al.'s sentiment analysis model
* data
	* Process and save Reddit SARC dataset to dynamoDB
	* `python save_csv.py` to save the coded csv files
	* `python save_json.py` to save the commments.json files
* dynamo
	* Python files that scans cleans and labels data in DynamoDB
	* These were used as sample code as a guideline for interacting with AWS DynamoDB
* myNLP
	* Clean, label and parse tweets to find emojis
	* `python cleanTweets.py` to clean
	* `python labelTweets.py` to label
	* `python EmojiParse.py` to parse emojis
* reddit
	* `python addFeatures.py` to get data from DynamoDB, use CoreNLP to generate features and upload them to DynamoDB
	* `python reddit_modeling.py` to train, test and evaluate models
* sentiment
	* Java code to use Stanford CoreNLP to engineer sentiment features
	* `SentimentAnalyzer.java` generates sentiment features given a piece of text
	* `SentimentAnalyzerEntryPoint.java` provides an entrypoint to the JVM allowing access from Python
* twitter
	* `python prepareDataset.py` to prepare the twitter dataset
	* `python streamTweets.py` to stream tweets using Twitter API
	* `python twitter_modeling.py` to train, test and evaluate ML models


