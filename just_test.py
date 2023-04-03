import json

with open('artile_info.json', 'r') as f:
            article = json.load(f)
articles = list(article)[:5]
print(articles)