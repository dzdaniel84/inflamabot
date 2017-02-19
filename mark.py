import markovify
import rake
import random

rake_object = rake.Rake("SmartStoplist.txt")


def bold(str):
    return '\033[1m{}\033[0m'.format(str)


def get_text(loc):  # ../Desktop/Barack Obama.txt
    with open(loc) as f:
        text = f.read()
    return text.replace('\n', '')


def run_rake(text):
    return [item[0] for item in rake_object.run(text) if
            ' ' not in item[0] and '\n' not in item[0]]


class Person:
    def __init__(self, name, loc):
        self.name = name
        self.text = get_text(loc)
        self.topics = {}
        #self.text_model = markovify.Text(self.text)
        #self.parse_sentences()

    # def parse_sentences(self):
    #     for i in range(500):
    #         try:
    #             t = self.text_model.make_sentence()
    #             items = run_rake(t)
    #             for i in items:
    #                 if i not in self.topics:
    #                     self.topics[i] = []
    #                 self.topics[i].append(t)
    #         except TypeError:
    #             continue

    def return_statement(self, text):
        text = [item for item in text.split(' ') if
                item in self.topics and len(self.topics[item])]
        if (len(text) == 0):
            return 'I have nothing to say'
        t = text[random.randint(0, len(text) - 1)]
        thing = self.topics[t][random.randint(0, len(self.topics[t]) - 1)]
        #self.topics[t].remove(thing)
        return thing

# washington = Person('Washington', 'people/washington.txt')
# obama = Person('Obama', 'people/obama.txt')
# stalin = Person('Stalin', 'people/stalin.txt')
# kanye = Person('Kanye', 'people/kanye.txt')
# trump = Person('Trump', 'people/trump.txt')
# fdroosevelt = Person('Roosevelt', 'people/fdroosevelt.txt')
# gwbush = Person('Bush', 'people/gwbush.txt')
# homer = Person('Homer', 'people/homer.txt')
# jackson = Person('Jackson', 'people/jackson.txt')
# kennedy = Person('Kennedy', 'people/kennedy.txt')
# lincoln = Person('Lincoln', 'people/lincoln.txt')
# reagan = Person('Reagan', 'people/reagan.txt')
# clinton = Person('Clinton', 'people/clinton.txt')

people = ['clinton', 'bush', 'homer', 'jackson', 'kanye', 'kennedy', 'lincoln',
          'obama', 'reagan', 'roosevelt', 'stalin', 'trump', 'washington']

def get_between():
    p1 = random.choice(people)
    p2 = random.choice(people)
    return (p1, p2)

def get_topic(first, second):
    return random.choice(list(first.topics.keys() | second.topics.keys()))

def convo(between, length=20):
    first, second = between
    start_text = get_topic(first, second)
    transcript = []
    first_copy, second_copy = first.topics.copy(), second.topics.copy()
    first_response, second_response = first.return_statement(start_text), ""
    transcript.append((0, first_response))
    while (
            first_response != 'I have nothing to say' and second_response != 'I have nothing to say'):
        second_response = second.return_statement(first_response)
        transcript.append((1, second_response))
        first_response = first.return_statement(second_response)
        transcript.append((0, first_response))
    first.topics, second.topics = first_copy, second_copy
    return transcript
