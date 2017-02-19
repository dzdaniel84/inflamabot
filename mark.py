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
    def __init__(self, name):
        self.name = name
        self.topics = {}
        #self.text_model = markovify.Text(self.text)
        #self.parse_sentences()

    @property
    def generated_file(self):
        return 'out/{}.txt'.format(self.name)

    @property
    def topics_file(self):
        return 'out/{}-topics.txt'.format(self.name)

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

    def shared_with(self, other):
        f1, f2 = open(self.topics_file, 'r'), open(other.topics_file, 'r')
        shared = []
        r1, r2 = f1.readline(), f2.readline()
        if r1 != '' and r2 != '':
            w1, w2 = r1.split(' ')[0], r2.split(' ')[0]
        while r1 != '' and r2 != '':
            if w1 > w2:
                r2 = f2.readline()
                if r2 != '':
                    w2 = r2.split(' ')[0]
            elif w2 > w1:
                r1 = f1.readline()
                if r1 != '':
                    w1 = r1.split(' ')[0]
            else:
                shared.append(w1)
                r1, r2 = f1.readline(), f2.readline()
                if r1 != '' and r2 != '':
                    w1, w2 = r1.split(' ')[0], r2.split(' ')[0]
        f1.close()
        f2.close()
        return shared

    def __repr__(self):
        return 'Person({})'.format(repr(self.name))

    def get_mappings(self, topics):
        f = open(self.topics_file, 'r')
        list_indices = []
        for line in f:
            s = line.split(' ')
            w = s[0]
            if w in topics:
                indices = [int(i) for i in s[1:]]
                list_indices.extend(indices)
        f.close()
        return list_indices

    def get_generated(self, i):
        f = open(self.generated_file)
        j = 0
        while j <= i:
            line = f.readline()
            j += 1
        return line.strip('\n')

    def return_statement(self, text):
        text = self.get_mappings(text.split(' '))
        if (len(text) == 0):
            return 'I have nothing to say'
        t = random.choice(text)
        return self.get_generated(t)

people = ['clinton', 'bush', 'homer', 'jackson', 'kanye', 'kennedy', 'lincoln',
          'obama', 'reagan', 'roosevelt', 'stalin', 'trump', 'washington', 'han', 'palin']

people = ['homer', 'kanye', 'lincoln',
          'obama', 'roosevelt', 'stalin', 'trump', 'washington', 'han', 'palin', 'deepak']

people = ['palin', 'deepak']

persons = [Person(person) for person in people]


def get_between():
    p1 = random.choice(persons)
    p2 = random.choice(persons)
    return (p1, p2)


def get_topic(p1, p2):
    return random.choice(p1.shared_with(p2))


def convo(between, length=20):
    first, second = between
    start_text = get_topic(first, second)
    transcript = []
    first_response, second_response = first.return_statement(start_text), ""
    transcript.append((0, first_response))
    while (first_response != 'I have nothing to say' and second_response != 'I have nothing to say' and len(transcript) < length):
        second_response = second.return_statement(first_response)
        transcript.append((1, second_response))
        first_response = first.return_statement(second_response)
        transcript.append((0, first_response))
    return transcript
