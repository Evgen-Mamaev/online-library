import argparse
import logging
import os
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup
from pathvalidate import sanitize_filename

logger = logging.getLogger(__file__)


def check_for_redirect(response_history):
    if response_history:
        raise requests.exceptions.HTTPError


def saves_book_txt(response, filename, folder='books/'):
    os.makedirs(folder, exist_ok=True)
    filename = sanitize_filename(filename)
    filepath = os.path.join(folder, filename)
    with open(filepath, 'wb') as file:
        file.write(response.content)


def download_book_cover(url_img, folder='images/'):
    filename = url_img.split('/')[-1]
    response = requests.get(url_img)
    response.raise_for_status()
    os.makedirs(folder, exist_ok=True)
    filepath = os.path.join(folder, filename)
    with open(filepath, 'wb') as file:
        file.write(response.content)


def parse_book_page(response):
    soup = BeautifulSoup(response.text, 'lxml')
    title_of_book, author = soup.find('h1').text.split('   ::   ')
    book_img = soup.find('div', class_='bookimage').find('img')['src']
    book_img_link = urljoin(response.url, book_img)
    comments = [comment.find('span', class_='black').text for comment in soup.find_all('div', class_='texts')]
    genres = [genre.text for genre in soup.find('span', class_='d_book').find_all('a')]
    book_page = {
        'title': title_of_book,
        'author': author,
        'cover': book_img_link,
        'comments': comments,
        'genres': genres,
    }
    return book_page


def sets_download_limits():
    parser = argparse.ArgumentParser(
        description='Введите номер начала и конца скачивания книг'
    )
    parser.add_argument('--start_id', default='0', help='Старт', type=int)
    parser.add_argument('--end_id', default='0', help='Стоп', type=int)
    return parser


def get_response_url_download_txt():
    url_download_txt = 'https://tululu.org/txt.php'
    payload = {'id': book_number}
    response_url_download_txt = requests.get(url_download_txt, params=payload)
    response_url_download_txt.raise_for_status()
    return response_url_download_txt


if __name__ == '__main__':
    parser = sets_download_limits()
    args = parser.parse_args()
    start_download = args.start_id
    stop_download = args.end_id + 1
    for book_number in range(start_download, stop_download):
        try:
            response_url_download_txt = get_response_url_download_txt()

            url_book = f'https://tululu.org/b{book_number}/'
            response_url_book = requests.get(url_book)
            response_url_book.raise_for_status()

            check_for_redirect(response_url_book.history)
            check_for_redirect(response_url_download_txt.history)

            book_page = parse_book_page(response_url_book)

            filename = f"{book_number}. {book_page.get('title')}.txt"
            saves_book_txt(response_url_download_txt, filename)

            url_img = book_page.get('cover')
            download_book_cover(url_img)

            logging.basicConfig(filename='sample.log', level=logging.INFO)
            logger.setLevel(logging.INFO)
            logger.info(f'Book number {book_number} loaded')
        except requests.exceptions.HTTPError:
            logger.info(f'Book number {book_number} is missing')
        except requests.ConnectionError:
            logging.basicConfig(filename='sample.log')
            logger.setLevel(logging.INFO)
            logger.error('Connection Error')
