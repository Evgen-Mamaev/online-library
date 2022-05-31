import os
import requests

for book in range(1, 11):
    url = f"https://tululu.org/txt.php?id={book}"

    response = requests.get(url)
    response.raise_for_status()

    os.makedirs("books", exist_ok=True)
    filename = f'books/id{book}.txt'
    with open(filename, 'wb') as file:
        file.write(response.content)
