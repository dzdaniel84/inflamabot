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
        self.text_model = markovify.Text(self.text)
        self.parse_sentences()

    def parse_sentences(self):
        for i in range(500):
            try:
                t = self.text_model.make_sentence()
                items = run_rake(t)
                for i in items:
                    if i not in self.topics:
                        self.topics[i] = []
                    self.topics[i].append(t)
            except TypeError:
                continue

    def return_statement(self, text):
        text = [item for item in text.split(' ') if
                item in self.topics and len(self.topics[item])]
        if (len(text) == 0):
            return 'I have nothing to say'
        t = text[random.randint(0, len(text) - 1)]
        thing = self.topics[t][random.randint(0, len(self.topics[t]) - 1)]
        self.topics[t].remove(thing)
        return thing


washington = Person('Washington', 'people/George Washington.txt')
obama = Person('Obama', 'people/Barack Obama.txt')
hitler = Person('Hitler', 'people/Adolf Hitler.txt')
stalin = Person('Stalin', 'people/Josef Stalin.txt')
kanye = Person('Kanye', 'people/Kanye West.txt')


def convo(first, second, start_text, length=20):
    first_copy, second_copy = first.topics.copy(), second.topics.copy()
    first_response, second_response = first.return_statement(start_text), ""
    while (
            first_response != 'I have nothing to say' and second_response != 'I have nothing to say'):
        print("{}: {}".format(bold(first.name.upper()), first_response))
        second_response = second.return_statement(first_response)
        print("{}: {}".format(bold(second.name.upper()), second_response))
        first_response = first.return_statement(second_response)
    first.topics, second.topics = first_copy, second_copy
