# Library of methods that extract emojis from text and
# also gets the sentiment score associated with emoji
# using emoji sentiment lexicon
import csv
import sys
import emoji

class EmojiParse:
	# return a tuple of string and list
	# string is text without emojis, list is a list of all emojis
	def extract_emojis(self, text):
		noEmoji = []
		emojis = []	
		for c in text:
			if c in emoji.UNICODE_EMOJI:
				emojis.append(c)
			else:
				noEmoji.append(c)
		noEmoji = ''.join(noEmoji)
		return (noEmoji, emojis)

	def emoji_parse(self, text):
		text, emojis = self.extract_emojis(text)
		em = []
		sentiment = []

		for e in emojis:
			if ord(e) in self.emoji_lexicon:
				em.append(e)
				sentiment.append(self.emoji_lexicon[ord(e)])

		return (text, em, sentiment)

	# sentiment score of emoji on a scale from 0 to 4
	# 0: very negative, 2: neutral, 4: very positive
	def sentiment_score(self, neg, neutral, pos):
		return (0 * neg + 2.0 * neutral + 4.0 * pos) / (neg + neutral + pos)

	def __init__(self):	
		# import emoji sentiment lexicon from csv file
		self.emoji_lexicon = {}

		f = open('../data/emoji/emoji_sentiment.csv', 'rt')	
		csv_reader = csv.reader(f)
		next(csv_reader) # skip csv header

		for row in csv_reader:
			_, hex, _, _, neg, neutral, pos, _, _ = row
			key = int(hex, 0)
			value = self.sentiment_score(int(neg), int(neutral), int(pos))
			self.emoji_lexicon[key] = value

def main():	
	emojiParse = EmojiParse()
	for line in sys.stdin:
		print(emojiParse.emoji_parse(line))

if __name__ == '__main':
	main()
