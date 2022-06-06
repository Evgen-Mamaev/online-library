from urllib.parse import urljoin
from urllib.parse import urlparse
from urllib.parse import urlsplit
import os
import requests
from bs4 import BeautifulSoup


def title_loading(url):
    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'lxml')
    title_book = soup.find('h1').text.split('   ::   ')[0]
    book_img = soup.find('div', class_='bookimage').find('img')['src']
    print(f'Заголовок: {title_book}')
    print(urljoin(url, book_img))


