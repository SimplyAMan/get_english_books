# -*- coding: utf-8 -*-
import urllib.request
from bs4 import BeautifulSoup
import web_utils
import os


def get_url(url, dest_path):
    soup_book = BeautifulSoup(urllib.request.urlopen(url))
    try:
        book_url = soup_book.find(
            'a', target='_self', title="Download book in epub").get('href')
        web_utils.download_file(book_url, dest_path)
    except AttributeError:
        pass
    finally:
        pass

    try:
        audio_url = soup_book.find(
            'a', target='_self', title='Download audiobook in mp3').get('href')
        web_utils.download_file(audio_url, dest_path)
    except AttributeError:
        pass
    finally:
        pass

if __name__ == "__main__":
    config = {
        'path': 'Output',
        'books': [
            {'book_level': 'Elementary',
             'book_url': 'http://english-e-books.net/elementary/'},
            {'book_level': 'Pre-Intermediate',
             'book_url': 'http://english-e-books.net/pre-intermediate/'},
            {'book_level': 'Intermediate',
             'book_url': 'http://english-e-books.net/intermediate/'},
            {'book_level': 'Upper-Intermediate',
             'book_url': 'http://english-e-books.net/upper-intermediate'},
            {'book_level': 'Advanced',
             'book_url': 'http://english-e-books.net/advanced/'}]}

    for book in config['books']:
        path = os.path.join(config['path'], book['book_level'])
        os.makedirs(path, exist_ok=True)
        contents = urllib.request.urlopen(book['book_url'])
        soup = BeautifulSoup(contents)
        content = soup.find('div', id='contentholder')
        table = content.find('table')
        for full_url in table.find_all('a', rel="bookmark"):
            get_url(full_url.get('href'), path)
