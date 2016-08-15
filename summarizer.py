import nltk.data
import nltk.stem.porter
import string

### Need to download nltk as well as the punkt tokenizer

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

class summarizer:
	def __init__(self):
		self.stemmer = nltk.stem.porter.PorterStemmer()
		self.word_count = self.count_words(full_text)
		self.sentence_list = self.split_text(full_text)
		self.sentence_scores = self.score(self.sentence_list, self.word_count)

	def strip_word(self, word):
		trans = str.maketrans({c: None for c in string.punctuation})
		new_word = word.translate(trans)
		return new_word.lower()


	def split_text(self, text):
		#text = "Hello, it's me. I was wondering if after all these years you'd like to meet."
		text = text.replace('.\n', '. ')
		text = text.replace('\n', '. ')
		sentence_tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
		list_of_sentences = sentence_tokenizer.tokenize(text.strip())
		return list_of_sentences

	def count_words(self, text):
		#text = "Hello, it's me! I was wondering if after all these years you'd like to meet. Hello can you hear me too."
		word_count = {}
		words = text.split()
		for word in words:
			word = self.strip_word(word)
			word = self.stemmer.stem(word)
			if word in word_count:
				word_count[word] += 1
			else:
				word_count[word] = 1
		return word_count

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

	def summarize(self, num):
		best_sentences = []
		scores = dict(self.sentence_scores)
		try:
			if num > len(scores):
				raise IndexError 
			for i in range(num):
				best = max(scores, key = lambda x: scores[x])
				best_sentences.append(best)
				scores.pop(best, None)
			for sentence in self.sentence_list:
				if sentence in best_sentences:
					print(sentence + '\n')
					best_sentences.remove(sentence)
		except IndexError:
			print("ERROR: Article does not have " + str(num) + " sentences. Article has " + str(len(self.sentence_scores)) + " sentences.")

	def ordered_summarize(self, num):
		best_sentences = []
		scores = dict(self.sentence_scores)
		try:
			if num > len(scores):
				raise IndexError 
			for i in range(num):
				best = max(scores, key = lambda x: scores[x])
				print(best + '\n')
				scores.pop(best, None)
		except IndexError:
			print("ERROR: Article does not have " + str(num) + " sentences. Article has " + str(len(self.sentence_scores)) + " sentences.")

	def return_keywords(self, num):
		pass


s = summarizer()
s.summarize(4)

###make method for ranking most to least important sentences-DONE
###remove stop words (common words like the, of, and, etc)
###make method for reducing by a certain percentage. eg. shorten by 80%
###make method to view top words


