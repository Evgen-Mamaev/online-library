from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup
from pprint import pprint

def title_loading(url):
    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'lxml')
    title_book = soup.find('h1').text.split('   ::   ')[0]
    book_img = soup.find('div', class_='bookimage').find('img')['src']
    print(f'Заголовок: {title_book}')
    print(urljoin(url, book_img))




def parse_book_page(url):
    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'lxml')
    title_book = soup.find('h1').text.split('   ::   ')[0]
    author = soup.find('h1').text.split('   ::   ')[1]
    book_img = soup.find('div', class_='bookimage').find('img')['src']
    book_img_link = urljoin('https://tululu.org/', book_img)
    comments = []
    for comment in soup.find_all('div', class_='texts'):
        text_comments = comment.find('span', class_='black')
        comments.append(text_comments.text)
    genres = []
    genres_soup = soup.find('span', class_='d_book').find_all('a')
    for genre in genres_soup:
        genres.append(genre.text)
    inf_book_page = {
        'name of the book': title_book,
        'book author': author,
        'book cover': book_img_link,
        'book comments': comments,
        'book genre': genres,
    }
    pprint(inf_book_page)






for book_number in range(3, 11):
    url = f'https://tululu.org/b{book_number}/'
    parse_book_page(url)

