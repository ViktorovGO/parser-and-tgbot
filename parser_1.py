import pip


import requests
from bs4 import BeautifulSoup
import time
import json
start = time.time()
global headers 
headers = {
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.2 Safari/605.1.15'
    }

def get_info(url=''):
    
    s = requests.Session()
    # response = s.get(url,headers = headers)
    # soup = BeautifulSoup(response.text,'lxml')
    # pagination_count = int(soup.find("ul", class_ = 'pagination').find('li', class_ = 'pagination__item pagination__link--right').text)
    
    articles_urls_list = []
    d = {}
    for page in range(1, 2):
        response = s.get(f'https://dota2.ru/news/?page={page}', headers = headers)
        soup = BeautifulSoup(response.text, 'lxml')
        articles_urls = soup.find_all('a', class_='index__news-link game-icon js-game-icon')
        
        for i, art_url in enumerate(articles_urls):
            art_url = 'https://dota2.ru'+art_url.get('href')
            art_id = art_url.split('-')[0].split('/')[-1]
            
            # articles_urls_list.append(art_url)
            response = s.get(art_url,headers = headers)
            soup = BeautifulSoup(response.text, 'lxml')
            
            
            title = soup.find('h1', class_ = 'title-global').text.strip()
            date_pub = soup.find('p', class_ = 'forum-theme__top-block-time').text.strip()
            text = soup.find('div', class_ = 'bg-main-block').find('div', class_  = 'global-content p-content js-text-errors-wrap').find_all('p')
            text = [block.text.replace('\xa0',' ') for block in text]
            text_str = '' # Текст статьи
            for txt in text:
                if txt!='':
                    text_str+=(txt.strip().replace('. ','.')+'\n\n')
            text = text_str
            img_art = soup.find('div', class_ = 'global-content p-content js-text-errors-wrap').find('img')["src"]
            # response = s.get(url = img_art)
            # with open(f'./imgs/{img_art.split("/")[-1]}','wb') as file:
            #     file.write(response.content)
            d[art_id]={
                    'original_url':art_url,
                    'title': title,
                    'date_pub': date_pub,
                    'text':text_str,
                    'img_art':img_art,
                    
                }

    with open('artile_info.json','w') as file:
            json.dump(d, file, indent = 4, ensure_ascii=False)
         
def get_fresh_news(url = ''):
    with open('artile_info.json','r') as f:
         list_of_articles = json.load(f)  
    s = requests.Session()
    new_articles = {}
    for page in range(1, 2):
        response = s.get(f'https://dota2.ru/news/?page={page}', headers = headers)
        soup = BeautifulSoup(response.text, 'lxml')
        articles_urls = soup.find_all('a', class_='index__news-link game-icon js-game-icon')

        for i, art_url in enumerate(articles_urls):
            art_url = 'https://dota2.ru'+art_url.get('href')
            art_id = art_url.split('-')[0].split('/')[-1]

            if art_id in list_of_articles:
                continue
            else:
                response = s.get(art_url,headers = headers)
                soup = BeautifulSoup(response.text, 'lxml')
                
                
                title = soup.find('h1', class_ = 'title-global').text.strip()
                date_pub = soup.find('p', class_ = 'forum-theme__top-block-time').text.strip()
                text = soup.find('div', class_ = 'bg-main-block').find('div', class_  = 'global-content p-content js-text-errors-wrap').find_all('p')
                text = [block.text.replace('\xa0',' ') for block in text]
                text_str = '' # Текст статьи
                for txt in text:
                    if txt!='':
                        text_str+=(txt.strip().replace('. ','.')+'\n\n')
                text = text_str
                img_art = soup.find('div', class_ = 'global-content p-content js-text-errors-wrap').find('img')["src"]
            
                new_articles[art_id]={
                        'original_url':art_url,
                        'title': title,
                        'date_pub': date_pub,
                        'text':text_str,
                        'img_art':img_art,
                        
                    }
                list_of_articles[art_id]={
                        'original_url':art_url,
                        'title': title,
                        'date_pub': date_pub,
                        'text':text_str,
                        'img_art':img_art,
                        
                    }
    with open('artile_info.json','w') as f:
         json.dump(list_of_articles, f, indent = 4, ensure_ascii=False)             
    
    return new_articles


def main():
    get_info('https://dota2.ru/news/')
    get_fresh_news('https://dota2.ru/news/')
    

if __name__=='__main__':
    main()
end = time.time()    
print(f'Отработал за {end-start} секунд')