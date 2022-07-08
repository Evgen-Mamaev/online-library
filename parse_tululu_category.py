from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

url_tululu = 'https://tululu.org/'
url_fantasy_genre_books = 'https://tululu.org/l55/1'
response_url_fantasy_genre_books = requests.get(url_fantasy_genre_books)
response_url_fantasy_genre_books.raise_for_status()
soup = BeautifulSoup(response_url_fantasy_genre_books.text, 'lxml')
book_number = soup.find('table', class_='d_book').find('a')['href']
url_book = urljoin(url_tululu, book_number)
print(url_book)
