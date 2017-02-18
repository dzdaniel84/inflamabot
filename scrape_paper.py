import newspaper
import json
import hashlib

download = True

def article_file(article):
    h = hashlib.sha256()
    h.update(article.url.encode())
    return 'articles/' + h.hexdigest() + '.json'

import sys

url = sys.argv[1]
leaning = sys.argv[2]

if download:

    breitbart = newspaper.build(url, memoize_articles=False)

    for article in breitbart.articles:
        print('hi')
        article.download()
        print(article)
        with open(article_file(article), 'w') as f:
            print(article_file(article))
            print('hi')
            json.dump({
                'url': article.url,
                'source_url': article.source_url,
                'title': article.title,
                'html': article.html,
                'source_type': leaning,
            }, f)