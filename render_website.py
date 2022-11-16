import json
from jinja2 import Environment, FileSystemLoader, select_autoescape
from livereload import Server
from more_itertools import chunked


def on_reload():
    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html'])
    )
    template = env.get_template('template.html')
    rendered_page = template.render(book_pages=book_pages_split_two)
    with open('index.html', 'w', encoding="utf8") as file:
        file.write(rendered_page)


filepath = r"""C:\Users\6000\Desktop\online-library\library\book_page.json"""
with open(filepath, "r", encoding="utf8") as file:
    book_page_json = file.read()
book_pages = json.loads(book_page_json)

book_pages_split_two = list(chunked(book_pages, 2))

on_reload()

server = Server()
server.watch('template.html', on_reload)
server.serve(root='.')
