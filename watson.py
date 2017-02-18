import sys
import os
import newspaper
from watson_developer_cloud import DiscoveryV1

discovery = DiscoveryV1(
  username="9d4dc181-a636-46c3-9e7a-48a60a9b0255",
  password="eIq0XfzlWdqI",
  version="2016-12-01"
)

environment_id = 'f8c120ac-c67a-4983-ba71-693704418700'
collection_id = '33821e0a-5fef-4675-9f98-478b6f49cbe7'

# see https://www.ibm.com/watson/developercloud/discovery/api/v1/?python#query-collection
def query(qopts={}):
    return discovery.query(environment_id, collection_id, qopts)

def add_from_url(url):
	def gen_filename():
		counter = 0
		while True:
			yield 'file{}.html'.format(counter)
			counter += 1
	
	paper, file_iter = newspaper.build(url, memoize_articles = False), gen_filename()
	for article in paper.articles:
		if('trump' in article.url.lower()):
			article.download()
			if article.html:
				filename = next(file_gen)
				f = open(filename, 'w+')
				f.write(article.html)
				f.close()
				add_document(filename)

def items(name, query):
	return [i[name] for i in query]

def add_document(filename):
	discovery.add_document(environment_id, collection_id, '../{}'.format(filename))
