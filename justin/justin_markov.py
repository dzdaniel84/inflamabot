import markovify
import os

with open(os.path.join(os.getcwd(), 'mein_kampf.txt')) as f:
    text = f.read()

text1 = markovify.Text(text)

with open(os.path.join(os.getcwd(), 'midsummer.txt')) as f:
    text = f.read()

text2 = markovify.Text(text)

combined = markovify.combine([text1, text2], [0.3, 1.5])


for i in range(5):
    print(text1.make_sentence_with_start("For"))
# get Trump's tweets
# find main idea of tweet
# train with Obama's tweet