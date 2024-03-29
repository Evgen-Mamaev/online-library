import json
import math
import os

from jinja2 import Environment, FileSystemLoader, select_autoescape
from livereload import Server
from more_itertools import chunked, ichunked


def on_reload():
    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html'])
    )
    template = env.get_template('template.html')
    total_catalogs = math.ceil(len(book_pages) / 20)
    book_page_chunks = ichunked(book_pages, 20)
    folder = "pages"
    os.makedirs(folder, exist_ok=True)
    for number, chunk in enumerate(book_page_chunks):
        catalog_number = number + 1
        book_pages_split_two = list(chunked(chunk, 2))
        rendered_page = template.render(
            book_pages=book_pages_split_two,
            catalog_number=catalog_number,
            total_catalogs=total_catalogs
        )
        filename = f'index{catalog_number}.html'
        filepath = os.path.join(folder, filename)
        with open(filepath, 'w', encoding="utf8") as file:
            file.write(rendered_page)


filepath = r"""C:\Users\6000\Desktop\online-library\library\book_page.json"""
with open(filepath, "r", encoding="utf8") as file:
    book_page_json = file.read()
book_pages = json.loads(book_page_json)

on_reload()

server = Server()
server.watch('template.html', on_reload)
server.serve(root='.')
