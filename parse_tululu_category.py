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


def saves_book_txt(response, filename, folder):
    os.makedirs(folder, exist_ok=True)
    filename = sanitize_filename(filename)
    filepath = os.path.join(folder, filename)
    with open(filepath, 'wb') as file:
        file.write(response.content)


def download_book_cover(img_url, folder):
    filename = img_url.split('/')[-1]
    response = requests.get(img_url)
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


def get_response_url_download_txt(url, payload):
    response_url_download_txt = requests.get(url, params=payload)
    response_url_download_txt.raise_for_status()
    return response_url_download_txt


def get_book_urls_answers_from_page(page_number):
    tululu_url = 'https://tululu.org/'
    fantasy_genre_book_urls = urljoin(tululu_url, f'/l55/{page_number}')
    fantasy_genre_book_response_urls = requests.get(fantasy_genre_book_urls)
    fantasy_genre_book_response_urls.raise_for_status()
    soup = BeautifulSoup(fantasy_genre_book_response_urls.text, 'lxml')
    book_numbers = [book_number['href'] for book_number in soup.select('.bookimage a')]
    book_urls = [urljoin(tululu_url, book_number) for book_number in book_numbers]
    return book_urls


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


def write_json(json_file, folder, filename):
    os.makedirs(folder, exist_ok=True)
    filename = sanitize_filename(filename)
    filepath = os.path.join(folder, filename)
    try:
        with open(filepath, 'r', encoding='utf8') as my_file:
            file = json.load(my_file)
    except FileNotFoundError:
        file = []
    file.append(json_file)
    with open(filepath, 'w', encoding='utf8') as my_file:
        json.dump(file, my_file, ensure_ascii=False, indent=2)


if __name__ == '__main__':
    logging.basicConfig(filename='sample.log', level=logging.INFO)
    logger.setLevel(logging.INFO)

    parser = sets_page_loading_options()
    args = parser.parse_args()
    download_start_page = args.start_page
    download_stop_page = args.end_page

    json_file = []
    for page_number in range(download_start_page, download_stop_page):
        try:
            book_urls = get_book_urls_answers_from_page(page_number)
            for book_url in book_urls:
                try:
                    book_number = book_url.split('/')[-2].replace('b', '')

                    response_book_url = requests.get(book_url)
                    response_book_url.raise_for_status()

                    book_page = parse_book_page(response_book_url)

                    book_page['book_path'] = ' '
                    if not args.skip_txt:
                        url_download_txt = 'https://tululu.org/txt.php'
                        payload = {'id': book_number}
                        response_url_download_txt = get_response_url_download_txt(url_download_txt, payload)
                        filename = f"{book_number}. {book_page.get('title')}.txt"
                        folder = os.path.join(args.dest_folder, 'book')
                        saves_book_txt(response_url_download_txt, filename, folder)
                        book_page['book_path'] = os.path.join(folder, filename)

                    img_filename = book_page.get('img_path')
                    book_page['img_path'] = ' '
                    if not args.skip_imgs:
                        img_url = book_page.get('cover')
                        folder = os.path.join(args.dest_folder, 'images')
                        download_book_cover(img_url, folder)
                        book_page['img_path'] = os.path.join(folder, img_filename)

                    json_file.append(book_page)

                    logger.info(f'Book number {book_number} loaded')
                except requests.exceptions.ConnectionError:
                    logger.error('Connection Error')
                    time.sleep(10)
        except requests.exceptions.HTTPError:
            logger.error('Page not found')
        except requests.exceptions.ConnectionError:
            logger.error('Connection Error')

    json_folder = args.dest_folder
    json_filename = f'{args.json_path}.json'
    write_json(json_file, json_folder, json_filename)
