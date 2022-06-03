import requests
from bs4 import BeautifulSoup


def title_loading(url):
    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'lxml')
    title_book = soup.find('h1').text.split('   ::   ')[0]
    return title_book

url = 'https://tululu.org/b1/'


title_loading(url)

#print(soup.find('img', class_='attachment-post-image')['src'])

#print(soup.find('div', class_='entry-content').text)