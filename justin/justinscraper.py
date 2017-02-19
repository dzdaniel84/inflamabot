import newspaper
import json, sys, os
from watson_developer_cloud import DiscoveryV1

# Watson stuff
discovery = DiscoveryV1(
  username="9d4dc181-a636-46c3-9e7a-48a60a9b0255",
  password="eIq0XfzlWdqI",
  version="2016-12-01"
)

# Watson stuff
environment_id = '59401ea6-3614-4c75-baae-90231dcadd6b'
collection_id = '776be5b8-d34c-4145-8f1a-0dd950a510b3'

# JSON stuff
JSON_FILE = "cnn_articles.json"

# Scraping stuff
cnn_paper = newspaper.build("http://cnn.com", memoize_articles=False)

# takes each article, creates a JSON file of the texts
def scrapeArticles(news_object): 
    i = 0
    for article in cnn_paper.articles: 
        article.download()
        if article.is_downloaded: # if article properly downloads, start creating file and uploading
            article.parse()
            try:
                # create a JSON file, add the file text to it, 
                file_name = str(cnn_paper.brand) + "{0}".format(i) + ".json" # e.g. cnn4.json
                with open(file_name, 'w') as f:
                    f.dump(article.text)
                # call addDocument() to add document to Discovery
                addDocument(file_name, JSON_FILE)
                i += 1
                # delete file
                os.remove(file_name)
            except UnicodeEncodeError:
                pass

# creates a dictionary mapping articles to keywords
def getKeyWords():
    articleKeywords = {}
    i = 0
    try:
        for article in cnn_paper.articles:
            article.download()
            if article.is_downloaded:
                article.parse()
                article.nlp()
                articleKeywords[article.title] = article.keywords
                print(i)
                i += 1
    except newspaper.article.ArticleException:
        pass
    print(articleKeywords)


##
# Create configuration for storing documents
# Add documents to configuration
    # scrape article
    # put article raw text in a json file
    # add article to collection

# takes in a JSON file name for the article, and the JSON_FILE that records what articles have been submitted, adds the document to Watson cloud
def addDocument(file_name, JSON_FILE):
    with open((os.path.join(os.getcwd(), '', file_name))) as fileinfo, open(JSON_FILE, 'w') as recording::
        # adds file to Waston API cloud
        try:
            add_doc = discovery.add_document(environment_id, collection_id, fileinfo=fileinfo)
            print(json.dumps(add_doc, indent=2))
        except:
            pass
        # records what file has been added
        recording.dump(file_name)
        recording.write('\n')



#writeToJSON(JSON_FILE)
scrapeArticles(cnn_paper)







