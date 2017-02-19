import sys
import os
import newspaper
from watson_developer_cloud import DiscoveryV1

discovery = DiscoveryV1(
    username="9d4dc181-a636-46c3-9e7a-48a60a9b0255",
    password="eIq0XfzlWdqI",
    version="2016-12-01"
)

environment_id = '59401ea6-3614-4c75-baae-90231dcadd6b'
collection_id = '776be5b8-d34c-4145-8f1a-0dd950a510b3'


# see https://www.ibm.com/watson/developercloud/discovery/api/v1/?python#query-collection
def query(qopts={'query': 'trump'}):
    return discovery.query(environment_id, collection_id, qopts)['results']


def add_from_url(url):
    def gen_filename():
        counter = 0
        while True:
            yield 'file{}.html'.format(counter)
            counter += 1

    paper, file_iter = newspaper.build(url,
                                       memoize_articles=False), gen_filename()

    for article in paper.articles:
        if ('trump' in article.url.lower()):
            article.download()
            if article.html:
                filename = next(file_iter)
                f = open(filename, 'w+')
                f.write(article.html)
                f.close()
                add_document(filename)


def items(name, query=query()):
    return [i[name] for i in query]


def add_document(filename):
    with open((os.path.join(os.getcwd(), '', filename))) as fileinfo:
        discovery.add_document(environment_id, collection_id, fileinfo=fileinfo)
