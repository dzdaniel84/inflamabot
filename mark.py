import markovify
import rake
import random

with open("file0.txt") as f:
    text = f.read()
text_model = markovify.Text(text)
rake_object = rake.Rake("SmartStoplist.txt")

def create_tweet():
	items = ['President', 'Trump', 'Russia']
	try:
		return text_model.make_sentence_with_start(items[random.randint(0, 2)])
	except KeyError:
		return text_model.make_sentence_with_start('Trump')

def run_rake():
	return [item for item in rake_object.run(text) if ' ' not in item[0] and '\n' not in item[0]][5:50]