"""
Define functions to label tweets as being sarcastic or not.
There are two ways this will be done.
1. Label as sarcastic if tweet contains #sarcasm or #sarcastic hashtag
2. Use already existing model (e.g. DeepMoji) to label tweet
"""

def hashtagLabel(tweet):
	"""Labels tweet as saracstic if it contains #sarcasm or #sarcastic
	Args:
		tweet (str): a single tweet
	Returns:
		True if tweet contains sarcasm hashtag, False otherwise
	"""
	if '#sarcasm' in tweet:
		return True
	if '#sarcastic' in tweet:
		return True
	return False

def test():
	sarcastic = "I love how the weather is great today #sarcasm"
	sarcastic2 = "I love justin bieber #sarcastic"
	genuine = "I love chocolate cake"
	words = [sarcastic, sarcastic2, genuine]
	print("Test hashtagLabel")
	for word in words:
		print(word + " " + str(hashtagLabel(word)))

if __name__ == "__main__":
	test()
