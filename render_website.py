import json
from jinja2 import Environment, FileSystemLoader, select_autoescape

env = Environment(
    loader=FileSystemLoader('.'),
    autoescape=select_autoescape(['html'])
)

template = env.get_template('template.html')

filepath = r"""C:\Users\6000\Desktop\online-library\library\book_page.json"""
with open(filepath, "r", encoding="utf8") as file:
    book_page_json = file.read()

book_pages = json.loads(book_page_json)

rendered_page = template.render(book_pages=book_pages)

with open('index.html', 'w', encoding="utf8") as file:
    file.write(rendered_page)
