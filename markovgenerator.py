import markovify
import random
import math
from mark import run_rake

def get_text(loc):
    with open(loc) as f:
        text = f.read()
    return text.replace('\n', '')


def create_text(name, url, out, len=10000):
    text_model = markovify.Text(get_text(url))
    f = open(out + '.txt', 'w+')
    print('{} progress: 0%'.format(name), end='\r')
    j = 0
    topics = {}
    for i in range(len):
        try:
            print('{} progress: {:6.3f}% [{}{}]'.format(name, i/len*100, '=' * j, ' ' * (10 - j)), end='\r')
            j = round((1 + math.sin(i/100)) * 5)
            t = text_model.make_sentence()
            items = run_rake(t)
            for topic in items:
                if topic not in topics:
                    topics[topic] = []
                topics[topic].append(str(i))
            f.write(t + '\n')
        except TypeError:
            continue
    f.close()
    with open(out + '-topics.txt', 'w+') as f:
        for t in sorted(topics):
            f.write(t + ' ' + ' '.join(topics[t]) + '\n')

people = ['clinton', 'bush', 'homer', 'jackson', 'kanye', 'kennedy', 'lincoln',
          'obama', 'reagan', 'roosevelt', 'stalin', 'trump', 'washington']
#people = ['trump']

def loadpeople():
    for person in people:
        create_text(person, 'people/{}.txt'.format(person), 'out/{}'.format(person))

if __name__ == '__main__':
    loadpeople()