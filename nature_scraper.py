import os

import requests
import string
from bs4 import BeautifulSoup

n_pages = int(input())
article_type = input()

HOME_URL = 'https://www.nature.com'

for i in range(1, n_pages + 1):
    r = requests.get(f'https://www.nature.com/nature/articles?sort=PubDate&year=2020&page={i}', headers={'Accept-Language': 'en-US,en;q=0.5'})

    article_dict = {
        'title': [],
        'link': []
    }

    if r.status_code != 200:
        print(f'The URL returned {r.status_code}!')
    else:
        page_directory = f"Page_{i}"
        os.makedirs(page_directory, exist_ok=True)

        soup = BeautifulSoup(r.text, 'html.parser')

        articles = soup.find_all('article')
        for article in articles:
            span_tag = article.find('span', class_='c-meta__type')
            if span_tag and span_tag.text == article_type:
                titles = [
                    '_'.join(
                        word.strip(string.punctuation)
                        for word in a_tag.text.split()
                        if word.strip(string.punctuation)
                    ) + '.txt'
                    for a_tag in article.find_all('h3') if a_tag.find('a')
                ]
                links = [HOME_URL+a_tag['href'] for a_tag in article.find_all('a', href=True)]
                article_dict['title'].extend(titles)
                article_dict['link'].extend(links)

        for title, link in zip(article_dict['title'], article_dict['link']):
            print("Title:", title)
            print("Link:", link)
            r = requests.get(link, headers={'Accept-Language': 'en-US,en;q=0.5'})
            soup = BeautifulSoup(r.text, 'html.parser')
            body = soup.find('p', class_='article__teaser')
            # print(title)
            file_path = os.path.join(page_directory, title)
            with open(file_path, 'wb') as file:
                file.write(body.string.strip().encode('utf-8'))
