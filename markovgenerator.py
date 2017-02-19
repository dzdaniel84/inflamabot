import markovify
import random
import math

def get_text(loc):
    with open(loc) as f:
        text = f.read()
    return text.replace('\n', '')


def create_text(name, url, out, len=100000):
    text_model = markovify.Text(get_text(url))
    f = open(out, 'w+')
    print('{} progress: 0%'.format(name), end='\r')
    j = 0
    for i in range(len):
        try:
            print('{} progress: {:6.3f}% [{}{}]'.format(name, i/len*100, '=' * j, ' ' * (10 - j)), end='\r')
            j = round((1 + math.sin(i/100)) * 5)
            f.write(text_model.make_sentence() + '\n')
        except TypeError:
            continue
    f.close()

people = ['bush', 'clinton', 'homer', 'jackson', 'kanye', 'kennedy', 'lincoln',
          'obama', 'reagan', 'roosevelt', 'stalin', 'trump', 'washington']
#people = ['trump']

def loadpeople():
    for person in people:
        create_text(person, 'people/{}.txt'.format(person), 'out/{}.txt'.format(person))

if __name__ == '__main__':
    loadpeople()