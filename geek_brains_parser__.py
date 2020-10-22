import requests
from bs4 import BeautifulSoup
import json
import uuid
import pymongo
from pymongo import MongoClient

class Parser_GeekBrains:

    def __init__(self, start_url, all_pages):
        self.all_pages = all_pages
        self.start_url = start_url
        mongo_client = MongoClient('mongodb://localhost:27017')
        self.db = mongo_client['geek_brains_parser']

    def get_soup(self, url):
        self.response = requests.get(url)
        self.soup = BeautifulSoup(self.response.text, 'lxml')
        return self.soup

    def get_all_pages(self):
        list_of_links = []
        list_of_pages = []
        for el in range(self.all_pages+1):
            list_of_pages.append(str(el))
        while len(list_of_pages) != len(list_of_links):
            for el in list_of_pages:
                list_of_links.append('https://geekbrains.ru/posts?page=' + el)
        return list_of_links

    def get_next_page(self, url):
        list_of_pages = []
        self.next_page = self.get_soup(url).find_all('a', attrs={'rel': 'next'})
        for el in self.next_page:
            href = 'https://geekbrains.ru/' + el.get('href')
            list_of_pages.append(href)
        # self.next_page_href = 'https://geekbrains.ru/' + self.next_page_href
        return list_of_pages


    def parse(self):

        geek_brains_post_structure = {
            'material_url': '',
            'header': '',
            'first_picture': '',
            'date_datetime': '',
            'autor_name': '',
            'autor_link': '',
        }

        geek_brains_comments_structure = {
            'autor_comment': '',
            'text_comment': '',
        }

        list_of_url = []
        for el in self.get_all_pages():
            self.material_without_url = self.get_soup(el).find_all('a', attrs={'class': 'post-item__title h3 search_text'})

            for material_with_url in self.material_without_url:
                material_with_url = material_with_url.get('href')
                geek_brains_post_structure['material_url'] = material_with_url
                list_of_url.append(material_with_url)

        return list_of_url

    def save_to(self, product_data):
        collection = self.db['geek_brains']
        collection.insert_one(product_data)

pg = Parser_GeekBrains("https://geekbrains.ru/posts", 60)

print('hi')
print(pg.get_all_pages())
print(pg.parse())
