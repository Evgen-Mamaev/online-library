import argparse
import os
from pprint import pprint
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup
from pathvalidate import sanitize_filename


def check_for_redirect(url):
    response = requests.get(url)
    response.raise_for_status()
    if response.url != url:
        raise requests.exceptions.HTTPError


def download_txt(url, filename, folder='books/'):
    response = requests.get(url)
    response.raise_for_status()
    os.makedirs(folder, exist_ok=True)
    filename = sanitize_filename(filename)
    filepath = os.path.join(folder, filename)
    with open(filepath, 'wb') as file:
        file.write(response.content)


def download_book_covers(url, folder='images/'):
    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'lxml')
    book_img = soup.find('div', class_='bookimage').find('img')['src']
    filename = book_img.split('/')[-1]
    url_img = urljoin('https://tululu.org/', book_img)
    response = requests.get(url_img)
    response.raise_for_status()
    os.makedirs(folder, exist_ok=True)
    filepath = os.path.join(folder, filename)
    with open(filepath, 'wb') as file:
        file.write(response.content)


def title_loading(url):
    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'lxml')
    title_book = soup.find('h1').text.split('   ::   ')[0]
    return title_book


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


def start_stop_download():
    parser = argparse.ArgumentParser(
        description='Введите номер начала и конца скачивания книг'
    )
    parser.add_argument('--start_id', default='0', help='Старт', type=int)
    parser.add_argument('--end_id', default='0', help='Стоп', type=int)
    return parser


if __name__ == '__main__':
    parser = start_stop_download()
    args = parser.parse_args()
    start_download = args.start_id
    stop_download = args.end_id
    for book_number in range(start_download, stop_download):
        try:
            url = 'https://tululu.org/'
            url_download_txt = f'https://tululu.org/txt.php?id={book_number}'
            url_book = f'https://tululu.org/b{book_number}/'
            check_for_redirect(url_download_txt)
            filename = f'{book_number}. {title_loading(url_book)}.txt'
            download_txt(url_download_txt, filename)
            download_book_covers(url_book)
            parse_book_page(url_book)
        except requests.exceptions.HTTPError:
            pass