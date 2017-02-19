import os
import json
import random
import collections

def one_in(n):
    return random.randrange(n) == 0

def split(t, seps):
    for s in seps:
        t = [w for e in t for w in e.split(s) if w != '']
    return t

exclude = ['the', 'to', 'of', 'and', 'a', '', 'in', 'that', 'for', 'on', 'is', 'with', 'was',
           'as', 'has', 'up', 'by', 'our', 'at', 'from', 'be', 'are', 'what', 'you', 'more', 'i',
           'an', 'who', 'will', 'we', 'also', 'or', 'and', 'if', 'into', 'before', 'can', 'many',
           'over', 'it', 'do', 'me', 'its']

def load_article(filename):
    with open(filename, 'r') as f:
        p = json.load(f)

    text = p['text'].replace('\n', '').replace('(', '').replace(')', '').replace('”', '')\
        .replace('“', '').replace("'s", '').replace(':', '').replace('-', '').replace(',', '')\
        .replace('"', '').lower()
    sentences = split([text], ['.', '!', '?'])
    wordss = [[w for w in s.split(' ') if w not in exclude] for s in sentences]
    return wordss, p['leaning']

articles = next(os.walk('articles/'))[2]

f = open('out.txt', 'w')

for article in articles:
    filename = 'articles/' + article
    a, l = load_article(filename)
    for s in a:
        if len(s) > 10 and random.random() > 0.95:
            f.write('"' + ' '.join(s) + '", ' + l + '\n')

f.close()