import nltk.stem.wordnet
import nltk.data
import nltk.stem.porter
import string

### Need to download nltk as well as the punkt tokenizer and corpora/wordnet
### Without lemmatizer/keyword display it can run faster

full_text = """

U.S.-backed fighters liberated a strategic Syrian city from the Islamic State over the weekend, bringing the rebels a step closer to the terrorist group's de facto capital of Raqqa and cutting off a route used by the militants.

Joyous residents of Manbij poured into the streets as the opposition forces continued to mop up pockets of resistance after weeks of intensive fighting and coalition bombing. Men shaved their beards, and women could walk outside without face coverings for the first time in years, according to videos posted from the war-torn city.

The Pentagon confirmed that the city was mostly in the hands of the coalition-backed Syrian Democratic Forces. American officers have said the battle was a key test for the more critical fight to drive the Islamic State from Raqqa.

Manbij was the main processing center for foreign fighters coming into the city to join the Islamic State and also a place where terrorists were sent to carry out operations outside the region.

“Manbij was a node that the enemy (used) for foreign fighter training and facilitation for external operations … outside of Iraq and Syria,” Army Lt. Gen. Sean MacFarland said last week in a briefing from Baghdad.

U.S. intelligence officials are analyzing thousands of items captured as Islamic State militants were fleeing the city in recent weeks, detailing the movement of foreign fighters in and out of the country, the Pentagon has said.

The battle for the city, which lasted several months, was also a test for the newly formed Syrian Democratic Forces, a collection of Kurdish and Arab forces organized to battle the Islamic State. The force is being advised by U.S. Special Operations Forces and supported by coalition airstrikes.

The battle in Manbij will “set the stage for the eventual attack to seize Raqqa and that will mark the beginning of the end" for the Islamic State in Syria, MacFarland said.

Opposition forces in Syria have captured about 20% of the territory controlled by the Islamic State at its peak last year. Progress has been faster in neighboring Iraq, where Iraqi forces have retaken at least 45% of the territory held by the Islamic State.

Earlier this year, the White House authorized the Pentagon to send several hundred additional U.S. personnel to help organize and advise the opposition forces in Syria.

It’s beginning to pay off. In Manbij Syrian opposition forces prevailed over a committed enemy who weren’t afraid to die and built elaborate defenses around the city.

“There are a lot of foreign fighters there and they haven't cut and run, at least not many of them,” MacFarland said in describing last week's fighting in Manbij. “They're fighting pretty hard in that city.”

The lessons learned in Manbij will help the opposition forces as they train and plan operations to drive the Islamic State from Raqqa, about 70 miles southeast of Manbij.

Air Force Lt. Gen. Jeffrey Harrigian, who commands U.S. air forces in the Middle East, said the U.S.-led coalition plans to attack Raqqa at the same time as Iraqi forces launch operations to liberate Mosul, Iraq's second largest city, from Islamic State control.

Any ground assaults on the cities are still months away, but Iraqi and Kurdish regional forces are moving into position to isolate the city in preparation for a battle to retake Mosul.

Forces aligned with the Kurdish regional government said Sunday in a statement they have retaken five villages east of Mosul. Iraqi government forces have been closing in on the city from the south.

"""
### Summarizer class has functions to summzarize a given text to a specified number of sentences or by a specified percentage. It also has functions that
### use common word filtering and can present results in both chronological order and in order of most to least significant.
class summarizer:
	### Initializes several important structures that contain data about the text, including the word count, filtered word count, sentence list,
	### number of words, sentence scores, and filtered sentences scores.
	def __init__(self):
		self.common_words = ["the", "be", "am", "is", "are", "being", "was", "were", "been", "to", "of", "and", "a", "in", "that", "have",
							 "I", "it", "for", "not", "on", "with", "he", "as", "you", "do", "at", "this", "but", "his", "by", "from", "they"
							 "we", "say", "her", "she", "or", "an", "will", "my", "one", "all", "would", "there", "their", "what"]
		self.stemmer = nltk.stem.porter.PorterStemmer()
		self.lemmatizer = nltk.stem.wordnet.WordNetLemmatizer()

		self.common_stems = [self.stemmer.stem(x) for x in self.common_words]

		self.word_count, self.stem_to_word = self.count_words(full_text)
		self.number_of_words = len(full_text.split())

		self.sentence_list = self.split_text(full_text)
		self.sentence_scores = self.score(self.sentence_list, self.word_count)

		self.filtered_word_count = self.filter_word_count()
		self.filtered_sentence_scores = self.score(self.sentence_list, self.filtered_word_count)

	### Takes a word and removes any puntuation from it and reduces it to all lower case. Returns the result
	def strip_word(self, word):
		trans = str.maketrans({c: None for c in string.punctuation})
		new_word = word.translate(trans)
		return new_word.lower()

	### Given a body of text, splits it into sentences using the nltk punkt tokenizer. Returns a list containing all the sentences.
	def split_text(self, text):
		text = text.replace('.\n', '. ')
		text = text.replace('\n', '. ')
		sentence_tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
		list_of_sentences = sentence_tokenizer.tokenize(text.strip())
		return list_of_sentences

	### Given a body of text, splits it into individual words and find the stem of each word. Then it counts how many times each stem appears
	### in the text and puts that into a dictionary. Returns this dictionary, word_count
	### Also returns a mapping of each word stem to its lemmatization as a dictionary, word_map
	def count_words(self, text):
		#text = "Hello, it's me! I was wondering if after all these years you'd like to meet. Hello can you hear me too."
		word_count = {}
		word_map = {}
		words = text.split()
		for word in words:
			word = self.strip_word(word)
			word_stem = self.stemmer.stem(word)
			word_lem = self.lemmatizer.lemmatize(word)
			if word_stem in word_count:
				word_count[word_stem] += 1
			else:
				word_count[word_stem] = 1
				word_map[word_stem] = word_lem
		return word_count, word_map

	### Given a list of sentences and scores for each word, calculates the score for each sentence by adding all the words in the sentence.
	### Returns a dictionary mapping each sentence to its calculated score.
	def score(self, sentences, word_score):
		sent_scores = {}
		for sentence in sentences:
			words = sentence.split()
			score = 0
			for word in words:
				word = self.strip_word(word)
				word = self.stemmer.stem(word)
				try:
					score += word_score[word]
				except KeyError:
					score += 0
			sent_scores[sentence] = score
		return sent_scores

	### Goes through a copy of the word_count dictionary and removes all common words from it, returning the new filtered dictionary
	def filter_word_count(self):
		filtered_word_count = {}
		for word in self.word_count:
			if word not in self.common_stems:
				filtered_word_count[word] = self.word_count[word]
		return filtered_word_count

	### Given a number of sentences, num, prints a summary of the text that is the given number of sentences long with the sentences in the
	### summary being ordered from most to least important
	def ordered_summarize(self, num):
		self.ordered_summarize_helper(self.sentence_scores, num)

	### Given a number of sentences, num, prints a summary of the text that is the given number of sentences long with the sentences in the
	### summary being ordered from most to least important. This summary does not consider common words when calculating the sentence scores.
	def filtered_ordered_summarize(self, num):
		self.ordered_summarize_helper(self.filtered_sentence_scores, num)

	### Given a percentage, percent, prints a summary of the text that roughly reduces the length of the text by the given percentage with the 
	### sentences in the summary being ordered from most to least important
	def ordered_summarize_p(self, percent):
		self.ordered_summarize_p_helper(self.sentence_scores, percent)

	### Given a percentage, percent, prints a summary of the text that roughly reduces the length of the text by the given percentage with the 
	### sentences in the summary being ordered from most to least important. This summary does not consider common words when calculating the 
	### sentence scores.
	def filtered_ordered_summarize_p(self, percent):
		self.ordered_summarize_p_helper(self.filtered_sentence_scores, percent)

	### Helper function that takes in a dictionary of sentence scores, sentence_scores, and a number of sentences, num, and prints out
	### the summary of the text that is the given number of sentences long in order of most to least important, using the sentence scores
	### in the given dictionary.
	def ordered_summarize_helper(self, sentence_scores, num):
		scores = dict(sentence_scores)
		try:
			if num > len(scores):
				raise IndexError 
			for i in range(num):
				best = max(scores, key = lambda x: scores[x])
				print(sentence_scores[best])
				print(best + '\n')
				scores.pop(best, None)
		except IndexError:
			print("ERROR: Article does not have " + str(num) + " sentences. Article has " + str(len(self.sentence_scores)) + " sentences.")

	### Helper function that takes in a dictionary of sentence scores, sentence_scores, and a percentage, percent, and prints out
	### the summary that reduces the text by roughly the percentage given, with sentences in order of most to least important, using the sentence scores
	### in the given dictionary.
	def ordered_summarize_p_helper(self, sentence_scores, percent):
		if percent >= 100 or percent < 10:
			print("ERROR: Percentage must be a number from 10 and 99")
		else:
			p = percent / 100
			limit = self.number_of_words * (1 - p)
			scores = dict(sentence_scores)
			total_words = 0
			while total_words <= limit:
				best = max(scores, key = lambda x: scores[x])
				print(sentence_scores[best])
				print(best + '\n')
				scores.pop(best, None)
				total_words += len(best.split())
			print("Article reduced by " + str(1 - (total_words / self.number_of_words)) + "%")

	### Given a number of sentences, num, prints out a summary of the text that is the given number of sentences, with the sentences in the same order
	### they appear in the text.
	def summarize(self, num):
		self.summarize_helper(self.sentence_scores, num)

	### Given a number of sentences, num, prints out a summary of the text that is the given number of sentences, with the sentences in the same order
	### they appear in the text. This summary does not consider common words when calculating the sentence scores.
	def filtered_summarize(self, num):
		self.summarize_helper(self.filtered_sentence_scores, num)

	### Given a percentage, percent, prints out a summary that reduces the text roughly by the given percentage, with the sentences in the same order
	### they appear in the text.
	def summarize_p(self, percent):
		self.summarize_p_helper(self.sentence_scores, percent)

	### Given a percentage, percent, prints out a summary that reduces the text roughly by the given percentage, with the sentences in the same order
	### they appear in the text. This summary does not consider common words when calculating the sentence scores.
	def filtered_summarize_p(self, percent):
		self.summarize_p_helper(self.filtered_sentence_scores, percent)

	### Helper function that takes in a dictionary of sentence scores, sentence_scores, and a number of sentences, num, and prints out
	### the summary of the text that is the given number of sentences long in chronological order, using the sentence scores
	### in the given dictionary.
	def summarize_helper(self, sentence_scores, num):
		best_sentences = []
		scores = dict(sentence_scores)
		try:
			if num > len(scores):
				raise IndexError 
			for i in range(num):
				best = max(scores, key = lambda x: scores[x])
				best_sentences.append(best)
				scores.pop(best, None)
			for sentence in self.sentence_list:
				if sentence in best_sentences:
					print(sentence_scores[sentence])
					print(sentence + '\n')
					best_sentences.remove(sentence)
		except IndexError:
			print("ERROR: Article does not have " + str(num) + " sentences. Article has " + str(len(self.sentence_scores)) + " sentences.")

	### Helper function that takes in a dictionary of sentence scores, sentence_scores, and a percentage, percent, and prints out
	### the summary that reduces the text by roughly the percentage given, with sentences in chronological order, using the sentence scores
	### in the given dictionary.
	def summarize_p_helper(self, sentence_scores, percent):
		if percent >= 100 or percent < 10:
			print("ERROR: Percentage must be a number from 10 and 99")
		else:
			p = percent / 100
			limit = self.number_of_words * (1 - p)
			best_sentences = []
			scores = dict(sentence_scores)
			total_words = 0
			while total_words <= limit:
				best = max(scores, key = lambda x: scores[x])
				best_sentences.append(best)
				scores.pop(best, None)
				total_words += len(best.split())
			for sentence in self.sentence_list:
				if sentence in best_sentences:
					print(sentence_scores[sentence])
					print(sentence + '\n')
					best_sentences.remove(sentence)
			print("Article reduced by " + str(1 - (total_words / self.number_of_words)) + "%")

	### Given a number, num, prints out that many of the top/most frequent words in the text.
	def print_keywords(self, num):
		try:
			self.print_keywords_helper(self.word_count, num)
		except IndexError:
			print("ERROR: Article does not have " + str(num) + " distinct words. Article has " + str(len(words_copy)) + " distinct words.")

	### Given a number, num, prints out that many of the top/most frequent words in the text, ignoring any words that are common English words.
	def print_filtered_keywords(self, num):
		try:
			self.print_keywords_helper(self.filtered_word_count, num)
		except IndexError:
			print("ERROR: Article does not have " + str(num) + " distinct non-common words. Article has " + str(len(filtered_words_copy)) + " distinct non-common words.")

	### Given a dictionary, word_count, and a number, num, finds the top num words in the dictionary and prints them along with their scores.
	def print_keywords_helper(self, word_count, num):
		words_copy = dict(word_count)
		if num > len(words_copy):
			raise IndexError 
		for i in range(num):
			best_stem = max(words_copy, key = lambda x: words_copy[x])
			best_word = self.stem_to_word[best_stem]
			print(best_word + " " + str(words_copy[best_stem]) + '\n')
			words_copy.pop(best_stem, None)



s = summarizer()
s.filtered_ordered_summarize_p(80)


###make method for ranking most to least important sentences-DONE
###remove stop words (common words like the, of, and, etc)-DONE
###make method for reducing by a certain percentage. eg. shorten by 80%-DONE
###make method to view top words-DONE


