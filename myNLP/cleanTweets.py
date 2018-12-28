"""
Define functions that are called to clean tweets.
There are multiple ways in which a tweet needs to be cleaned.
1. Remove tweets with @mention at the start
2. Remove tweets with urls
3. Convert all characters to lowercase
4. Remove all other @mention within the text
5. Remove hashtag and leave word
"""
def isRetweet(text):
        """
        text : str
            text of tweet
        returns boolean, true if tweet is retweet
        """
        if 'RT @' in text:
            return True
        else:
            return False

def startsWithMention(tweet):
	"""Determines whether tweet starts with @mention
	Args:
		tweet (str): a single tweet
	Returns:
		bool: True if tweets starts with @mention, False otherwise
	"""
	if tweet[0] == '@':
		return True
	return False

def containsURL(tweet):
	"""Determines whether tweet contains URL
	Args:
		tweet (str): a single tweet
	Returns:
		bool: True if tweet contains URL, False otherwise
	"""
	if 'http' in tweet:
		return True
	if 'www' in tweet:
		return True
	return False

def toLowerCase(tweet):
	"""Converts tweet string to all lowercase characters
	Args:
		tweet (str): a single tweet
	Returns:
		str: all lowercase representation
	"""
	return tweet.lower()

def removeMention(tweet):
	"""Remove all @mention from tweet
	Args:
		tweet (str): a single tweet
	Returns:
		str: tweet with all mentions deleted
	"""
	words = tweet.split()
	removed = [word for word in words if word[0] != '@']
	return ' '.join(removed)

# must be called after removeHashtagSarcasm
def removeHashtag(tweet):
	"""Remove all hashtags from tweet
	Args:
		tweet (str): a single tweet
	Returns:
		str: tweet with all # removed, do not remove the
		text part of the hashtag
	"""
	words = tweet.split()
	for i in range(len(words)):
		if words[i][0] == '#':
			words[i] = words[i][1:]
	return ' '.join(words)

def removeHashtagSarcasm(tweet):
	tweet = tweet.replace("#sarcasm", "")
	tweet = tweet.replace("#sarcastic", "")
	return tweet

# Replace '&amp;' with 'and'
def replaceAmp(text):
    """
    Takes in string and returns string with '&amp;' replaced with 'and'
    """
    return text.replace('&amp;', 'and')

def removeLTGT(text):
	text = text.replace('&lt;', '')
	text = text.replace('&gt;', '')
	return text

def test():
	hashtag = "I am being #sarcastic #lol &lt; less than &gt; greater"
	print(hashtag)
	hashtag = removeHashtagSarcasm(hashtag)
	print(hashtag)
	hashtag = removeHashtag(hashtag)
	print(hashtag)
	hashtag = removeLTGT(hashtag)
	print(hashtag)
	# print("Test startsWithMention:")
	# noMention = "Hello world!"
	# mention = "@world hello"
	# print(noMention + ": " + str(startsWithMention(noMention)))
	# print(mention + ": " + str(startsWithMention(mention)))

	# print("\nTest containsURL:")
	# noURL = "Hello world!"
	# url = "hello world! https://www.bbc.com/"
	# print(noURL + ": " + str(containsURL(noURL)))
	# print(url + ": " + str(containsURL(url)))

	# print("\nTest toLowerCase:")
	# upperCase = "Hello World!!"
	# print(upperCase + "->" + toLowerCase(upperCase))

	# print("\nTest removeMention:")
	# mention = "hello @realTrump. Hello @bieber"
	# print(mention + "->" + removeMention(mention))

	# print("\nTest removeHashtag:")
	# hashtag = "great time in #korea #kbbq #bestPlaceEver"
	# print(hashtag + "->" + removeHashtag(hashtag))
	# sarcasmHashtag = "i love the weather in england #sarcasm not really"
	# print(sarcasmHashtag + "->" + removeHashtag(sarcasmHashtag))
	return

if __name__ == "__main__":
	test()

