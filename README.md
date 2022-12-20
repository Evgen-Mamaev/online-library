# Сайт для просмотра и выбора книг 

Пройдя по ссылке [Online-library](https://evgen-mamaev.github.io/online-library/pages/index1.html) вы можете ознакомиться со страницей для просмотра и выбора книг.
На странице представлены первые 100 книг с сайта [tululu.org](https://tululu.org/) в жанре "фантастика".


Для запуска сайта у себя на компьютере необходимо скачать папки с фалами: 
```
library
pages
static
```
И запустить любой файл из папки `pages`


# Парсер книг с сайта tululu.org

Проект предназначен для скачивания книг в жанре "фантастика" в формате .txt с сайта [tululu.org](https://tululu.org/)

## Запуск

Для запуска программы у вас уже должен быть установлен Python 3.

- Скачайте код
- Установите зависимости командой:

```Python
pip install -r requirements.txt
```

- Запустите программу командой:

```Python
parse_tululu_category.py --start_page=0 --end_page=702
```

, указав значения аргументов `--start_page` и `--end_page`

## Аргументы

При запуске программы, необходимо передать агрументы:

- `--start_page=` - передать номер страницы, с которой начнется скачивание (на странице 25 книг)
    * по умолчанию значение установлено на `1` (скачивание начнется с первой страницы)
- `--end_page=` - передать номер id книги, на которой остановится скачивание
    * по умолчанию значение установлено на `702` (последняя странница)
- `--dest_folder=` - можно указать папку для скачивания
    * по умолчанию скачивание начнется в папку `library`
- `--skip_imgs` - если скачивание картинок не требуется
- `--skip_txt` - если скачивание книг не требуется
- `--json_path=` - можно указать имя `.json` файла с информацией о книгах
    * по умолчанию имя файла `book_page`

## Пример выполнения

`parse_tululu_category.py --start_page=1 --end_page=2`

Программа создаст в каталоге где находится файл:

- папки по пути `/library/books`, загрузит файлы с текстами книги (25 книг) в формате `.txt`
    * `1. Название книги.txt` (Номер id. Название книги.txt)
- папки по пути `/library/images`, загрузит картинки с обложками книг (при наличии)
    * `1.jpg` (Номер id.формат картинки)
- файл по пути `/library/book_page.json`, запишет в него информацию о книгах в формате:

```Python
[
    {
        'title': ' ',
        'author': ' ',
        'cover': ' ',
        'img_path': ' ',
        'comments': ' ',
        'genres': ' ',
        'book_path': ' '  
    }
]
```

# Создание страниц со скаченными книгами

Проект предназначен для создания страницы для просмотра и чтения книг

## Запуск

- Скачайте книги из прошлого шага
- Запустите программу командой:

```Python
render_website.py
```

Программа создаст в папке `pages` страницы со скаченными книгами 

Внешний вид вкладки для просмотра книг:

![/Внешний вид карточки книги.png](https://github.com/Evgen-Mamaev/online-library/blob/main/%D0%92%D0%BD%D0%B5%D1%88%D0%BD%D0%B8%D0%B9%20%D0%B2%D0%B8%D0%B4%20%D0%BA%D0%B0%D1%80%D1%82%D0%BE%D1%87%D0%BA%D0%B8%20%D0%BA%D0%BD%D0%B8%D0%B3%D0%B8.png)


## Цель проекта

Выполнение задания к курсу, "Вёрстка для питониста" [dvmn.org](https://dvmn.org/)
