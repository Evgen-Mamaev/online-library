import os

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


def title_loading(url):
    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'lxml')
    title_book = soup.find('h1').text.split('   ::   ')[0]
    return title_book


for book_number in range(1, 11):
    try:
        url_download = f'https://tululu.org/txt.php?id={book_number}'
        url_book = f'https://tululu.org/b{book_number}/'
        check_for_redirect(url_download)
        filename = f'{book_number}. {title_loading(url_book)}.txt'
        download_txt(url_download, filename)
    except requests.exceptions.HTTPError:
        pass
