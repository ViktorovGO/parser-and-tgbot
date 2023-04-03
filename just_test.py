import json

from botttt import get_fresh_news

articles = get_fresh_news('https://dota2.ru/news/')

if articles!={}:
    for key in articles.keys():
        print(articles[key])