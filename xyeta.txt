import requests
from bs4 import BeautifulSoup
import json
import uuid

class Parser_GeekBrains:

    def __init__(self, start_url):
        self.start_url = start_url

    def get_response(self):
        self.response = requests.get(self.start_url)
        return self.response

    def get_soup(self):
        self.soup = BeautifulSoup(self.get_response().text, 'lxml')
        return self.soup

    def dict_name_generator(self):
        self.number = uuid.uuid4()
        return self.number

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

        self.material_without_url = self.get_soup().find_all('a', attrs={'class': 'post-item__title h3 search_text'})
        list_of_url = []
        for self.material_with_url in self.material_without_url:
            self.material_with_url = self.material_with_url.get('href')
            list_of_url.append(self.material_with_url)

            for el in list_of_url:
                geek_brains_post_structure['material_url'] = el
                print(geek_brains_post_structure)
        return geek_brains_post_structure


            # print(self.material_with_url)



    

pg = Parser_GeekBrains("https://geekbrains.ru/posts")
print('hi')
print(pg.parse())
print(pg.get_response())
print(pg.dict_name_generator())
# print(pg.get_soup())

# print(requests.get('https://geekbrains.ru/posts'))