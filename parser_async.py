
import requests
import asyncio
import aiohttp
import time
from datetime import datetime
from bs4 import BeautifulSoup

import json
start = time.time()
global headers 
headers = {
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.2 Safari/605.1.15'
    }

async def get_info_from_response(s, page):
    
    async with s.get(f'https://dota2.ru/news/?page={page}', headers = headers, ssl=False) as response:

        soup = BeautifulSoup(await response.text(), 'lxml')
        articles_urls = soup.find_all('a', class_='index__news-link game-icon js-game-icon')
        try:
            zakrep = soup.find('div', class_ = 'gradient-btn index__news-block-pinned').text.strip()
        except AttributeError:
            zakrep = ""
        
    for i, art_url in enumerate(articles_urls[:2]):
        art_url = 'https://dota2.ru'+art_url.get('href')
        # articles_urls_list.append(art_url)
        
        async with s.get(art_url,headers = headers,ssl=False) as response:
            soup = BeautifulSoup(await response.text(), 'lxml')
            
            
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
            if i==0:
                d.append(
                    {   
                        'original_url':art_url,
                        'title': title,
                        'date_pub': date_pub,
                        'text':text_str,
                        'img_art':img_art,
                        'zakrep':zakrep
                    }
                )
            else:
                d.append(
                    {   
                        
                        'original_url':art_url,
                        'title': title,
                        'date_pub': date_pub,
                        'text':text_str,
                        'img_art':img_art,
                        'zakrep':""
                    }
                )
      
    print(f'Обработал {page}/{pagination_count} страниц')          
    
    


async def get_tasks(url=''):
    async with aiohttp.ClientSession() as s:
        response = await s.get(url,headers = headers, ssl=False)
        soup = BeautifulSoup(await response.text(),'lxml')
        global pagination_count
        pagination_count = int(soup.find("ul", class_ = 'pagination').find('li', class_ = 'pagination__item pagination__link--right').text)
        global d
        articles_urls_list = []
        d = []
        
        
        tasks = []
        for page in range(1, 50):
            tasks.append(asyncio.create_task(get_info_from_response(s, page)))

        await asyncio.gather(*tasks)
    
    with open('artile_info_async.json','w') as file:
        json.dump(d, file, indent = 4, ensure_ascii=False, default=str)
        
    
    

    # with open('urls_list','w') as file:
    #     for url in articles_urls_list:    
    #         file.write(f'{url}\n')    

    # with open('index.html','w') as file:
    #     file.write(response.text)


def main():
    asyncio.run(get_tasks('https://dota2.ru/news/'))
      
    # get_info_article('urls_list')

if __name__=='__main__':
    main()
end = time.time()   
print(f'Отработал за {end-start} секунд') 