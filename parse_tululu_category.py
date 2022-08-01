import argparse
import json
import logging
import os
import time
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup
from pathvalidate import sanitize_filename

logger = logging.getLogger(__file__)


def check_for_redirect(response_history):
    if response_history:
        raise requests.exceptions.HTTPError


def saves_book_txt(response, filename, folder):
    os.makedirs(folder, exist_ok=True)
    filename = sanitize_filename(filename)
    filepath = os.path.join(folder, filename)
    with open(filepath, 'wb') as file:
        file.write(response.content)


def download_book_cover(url_img, folder):
    filename = url_img.split('/')[-1]
    response = requests.get(url_img)
    response.raise_for_status()
    os.makedirs(folder, exist_ok=True)
    filepath = os.path.join(folder, filename)
    with open(filepath, 'wb') as file:
        file.write(response.content)


def parse_book_page(response):
    soup = BeautifulSoup(response.text, 'lxml')
    title_of_book, author = soup.select_one('h1').text.split('   ::   ')
    book_img = soup.select_one('.bookimage img')['src']
    book_img_link = urljoin(response.url, book_img)
    comments = [comment.text for comment in soup.select('.texts .black')]
    genres = [genres.text for genres in soup.select('span.d_book a')]
    img_path = book_img.split('/')[-1]
    book_page = {
        'title': title_of_book,
        'author': author,
        'cover': book_img_link,
        'img_path': img_path,
        'comments': comments,
        'genres': genres
    }
    return book_page


def get_response_url_download_txt():
    url_download_txt = 'https://tululu.org/txt.php'
    payload = {'id': book_number}
    response_url_download_txt = requests.get(url_download_txt, params=payload)
    response_url_download_txt.raise_for_status()
    return response_url_download_txt


def get_response_url_books(number_page):
    url_tululu = 'https://tululu.org/'
    url_fantasy_genre_books = f'https://tululu.org/l55/{number_page}'
    response_url_fantasy_genre_books = requests.get(url_fantasy_genre_books)
    response_url_fantasy_genre_books.raise_for_status()
    soup = BeautifulSoup(response_url_fantasy_genre_books.text, 'lxml')
    book_numbers = [book_number['href'] for book_number in soup.select('.bookimage a')]
    url_books = [urljoin(url_tululu, book_number) for book_number in book_numbers]
    return url_books


def sets_page_loading_options():
    parser = argparse.ArgumentParser(
        description='Введите номер страницы начала и конца скачивания книг'
    )
    parser.add_argument('--start_page', default='1', help='Старт', type=int)
    parser.add_argument('--end_page', default='702', help='Стоп', type=int)
    parser.add_argument('--dest_folder', default='library', help='Укажите папку, для скаивания')
    parser.add_argument('--skip_imgs', help='Скачать обложки?', action='store_true')
    parser.add_argument('--skip_txt', help='Скачать книги?', action='store_true')
    parser.add_argument('--json_path', default='book_page', help='Укажите имя, для json')
    return parser


def write_json(book_page, folder, filename):
    os.makedirs(folder, exist_ok=True)
    filename = sanitize_filename(filename)
    filepath = os.path.join(folder, filename)
    try:
        with open(filepath, 'r', encoding='utf8') as my_file:
            file = json.load(my_file)
    except:
        file = []
    file.append(book_page)
    with open(filepath, 'w', encoding='utf8') as my_file:
        json.dump(file, my_file, ensure_ascii=False, indent=2)


if __name__ == '__main__':
    logging.basicConfig(filename='sample.log', level=logging.INFO)
    logger.setLevel(logging.INFO)

    parser = sets_page_loading_options()
    args = parser.parse_args()
    download_start_page = args.start_page
    download_stop_page = args.end_page

    for number_page in range(download_start_page, download_stop_page):
        url_books = get_response_url_books(number_page)
        for url_book in url_books:
            book_number = url_book.split('/')[-2].replace('b', '')
            try:
                response_url_book = requests.get(url_book)
                response_url_book.raise_for_status()

                check_for_redirect(response_url_book.history)

                book_page = parse_book_page(response_url_book)

                if not args.skip_txt:
                    response_url_download_txt = get_response_url_download_txt()
                    filename = f"{book_number}. {book_page.get('title')}.txt"
                    folder = f'{args.dest_folder}/book'
                    saves_book_txt(response_url_download_txt, filename, folder)
                    book_page['book_path'] = f'{folder}/{filename}'
                else:
                    book_page['book_path'] = ' '

                if not args.skip_imgs:
                    url_img = book_page.get('cover')
                    folder = f'{args.dest_folder}/images'
                    download_book_cover(url_img, folder)
                    book_page['img_path'] = f"{folder}/{book_page.get('img_path')}"
                else:
                    book_page['img_path'] = ' '

                folder_json = args.dest_folder
                filename_json = f'{args.json_path}.json'

                write_json(book_page, folder_json, filename_json)

                logger.info(f'Book number {book_number} loaded')
            except requests.exceptions.HTTPError:
                logger.info(f'Book number {book_number} is missing')
            except requests.ConnectionError:
                logger.error('Connection Error')
                time.sleep(10)
