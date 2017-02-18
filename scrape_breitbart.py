import newspaper
import json
import hashlib

download = True

def article_file(article):
    h = hashlib.sha256()
    h.update(article.url.encode())
    return 'articles/' + h.hexdigest() + '.json'

if download:

    breitbart = newspaper.build('http://huffingtonpost.com', memoize_articles=False)

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
                'source_type': 'conservative',
            }, f)