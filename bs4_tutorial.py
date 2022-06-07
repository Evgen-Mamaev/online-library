from urllib.parse import urljoin

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




def print_text_comments(url):
    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'lxml')
    title_book = soup.find('h1').text.split('   ::   ')[0]
    print(title_book)
    comments = []
    genres = []
    for comment in soup.find_all('div', class_='texts'):
        text_comments = comment.find('span', class_='black')
        comments.append(text_comments.text)
    print(*comments, sep='\n')
    genres_soup = soup.find('span', class_='d_book').find_all('a')
    for genre in genres_soup:
        genres.append(genre.text)
    print(genres)

    #print(*genres, sep='\n')

for book_number in range(3, 11):
    url = f'https://tululu.org/b{book_number}/'
    print_text_comments(url)

