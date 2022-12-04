import json
from jinja2 import Environment, FileSystemLoader, select_autoescape
from livereload import Server
from more_itertools import chunked, ichunked
import os


def on_reload():
    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html'])
    )
    template = env.get_template('template.html')
    book_page_chunks = ichunked(book_pages, 20)
    folder = "pages"
    os.makedirs(folder, mode=0o777, exist_ok=True)
    for catalog_number, chunk in enumerate(book_page_chunks):
        book_pages_split_two = list(chunked(chunk, 2))
        rendered_page = template.render(book_pages=book_pages_split_two)
        filename = f'index{catalog_number + 1}.html'
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
