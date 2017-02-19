import newspaper
import json
import hashlib
from newspaper import news_pool

def article_file(article):
    h = hashlib.sha256()
    h.update(article.url.encode())
    return 'articles/' + h.hexdigest() + '.json'

papers = [
    ('slate', 'liberal', 'http://slate.com')
]

for name, leaning, url in papers:

    paper = newspaper.build(url, memoize_articles=False)
    l = len(paper.articles)
    i = 0
    for article in paper.articles:
        print(name, '{}/{}'.format(i, l))
        article.download()
        article.parse()
        with open(article_file(article), 'w') as f:
            json.dump({
                'url': article.url,
                'source_url': article.source_url,
                'title': article.title,
                'text': article.text,
                'source': name,
                'leaning': leaning,
            }, f)
        i += 1