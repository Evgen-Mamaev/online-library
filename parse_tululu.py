import argparse
import os
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup
from pathvalidate import sanitize_filename


def check_for_redirect(response_history):
    if response_history:
        raise requests.exceptions.HTTPError


def download_txt(response, filename, folder='books/'):
    os.makedirs(folder, exist_ok=True)
    filename = sanitize_filename(filename)
    filepath = os.path.join(folder, filename)
    with open(filepath, 'wb') as file:
        file.write(response.content)


def download_book_covers(response, folder='images/'):
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


def title_loading(response):
    soup = BeautifulSoup(response.text, 'lxml')
    title_of_book, author = soup.find('h1').text.split('   ::   ')
    return title_of_book


def parse_book_page(response):
    soup = BeautifulSoup(response.text, 'lxml')
    title_of_book, author = soup.find('h1').text.split('   ::   ')
    book_img = soup.find('div', class_='bookimage').find('img')['src']
    book_img_link = urljoin('https://tululu.org/', book_img)
    comments = [comment.find('span', class_='black').text for comment in soup.find_all('div', class_='texts')]
    genres = [genre.text for genre in soup.find('span', class_='d_book').find_all('a')]
    book_page = {
        'title': title_of_book,
        'author': author,
        'cover': book_img_link,
        'comments': comments,
        'genres': genres,
    }
    # pprint(inf_book_page)
    print(f"Название: {book_page['title']}")
    print(f"Автор: {book_page['author']}")
    print()


def sets_download_limits():
    parser = argparse.ArgumentParser(
        description='Введите номер начала и конца скачивания книг'
    )
    parser.add_argument('--start_id', default='0', help='Старт', type=int)
    parser.add_argument('--end_id', default='0', help='Стоп', type=int)
    return parser


if __name__ == '__main__':
    parser = sets_download_limits()
    args = parser.parse_args()
    start_download = args.start_id
    stop_download = args.end_id + 1
    for book_number in range(start_download, stop_download):
        try:
            url = 'https://tululu.org/'
            url_download_txt = f'https://tululu.org/txt.php?id={book_number}'
            response_url_download_txt = requests.get(url_download_txt)
            response_url_download_txt.raise_for_status()
            url_book = f'https://tululu.org/b{book_number}/'
            response_url_book = requests.get(url_book)
            response_url_book.raise_for_status()

            check_for_redirect(response_url_download_txt.history)

            filename = f'{book_number}. {title_loading(response_url_book)}.txt'
            download_txt(response_url_download_txt, filename)
            download_book_covers(response_url_book)
            parse_book_page(response_url_book)
        except requests.exceptions.HTTPError:
            pass
