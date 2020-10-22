import requests
from bs4 import BeautifulSoup
import json
import uuid
import pymongo
from pymongo import MongoClient

class Parser_GeekBrains:

    def __init__(self, start_url):
        self.start_url = start_url
        mongo_client = MongoClient('mongodb://localhost:27017')
        self.db = mongo_client['geek_brains_parser']

    def get_response(self):
        self.response = requests.get(self.start_url)
        return self.response

    def get_soup(self):
        self.soup = BeautifulSoup(self.get_response().text, 'lxml')
        return self.soup


    def save_to(self, product_data):
        collection = self.db['geek_brains']
        collection.insert_one(product_data)

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

        def uuid_gen():
            uuidGen = uuid.uuid4()
            return uuidGen

        self.material_without_url = self.get_soup().find_all('a', attrs={'class': 'post-item__title h3 search_text'})
        list_of_url = []
        for self.material_with_url in self.material_without_url:
            self.material_with_url = self.material_with_url.get('href')
            # geek_brains_post_structure['material_url'] = self.material_with_url
            list_of_url.append(self.material_with_url)
            # self.save_to(geek_brains_post_structure)

        for el in list_of_url:
            geek_brains_post_structure['material_url'] = el
            self.save_to(geek_brains_post_structure)

        return geek_brains_post_structure


    

pg = Parser_GeekBrains("https://geekbrains.ru/posts")
print('hi')
print(pg.parse())
print(pg.get_response())
