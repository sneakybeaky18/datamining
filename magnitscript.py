from bs4 import BeautifulSoup
import requests
from urllib.parse import urlparse
from pymongo import MongoClient



mongo_client = MongoClient('mongodb://localhost:27017')
db = mongo_client['parse_10']

dict = {
    'url': '',
    'promo_name': '',
    'product_name': '',
    'old_price': '',
    'new_price': '',
    'image_url': '',
    'date_from': '',
    'date_to': '',
}

def get_soup(url):
    params = {
        'geo': 'moskva',
    }
    response = requests.get(url, params)
    soup = BeautifulSoup(response.text, 'lxml')
    return soup

soup = get_soup('https://magnit.ru/promo/')

list_new_price = [] #получаем новую цену
for el in soup.find_all('div', attrs={'class': 'label__price_new'}):
    list_new_price.append(el.text)
dict['new_price'] = list_new_price

list_old_price = [] #получаем старую цену
for el in soup.find_all('div', attrs={'class': 'label__price_old'}):
    list_old_price.append(el.text)
dict['old_price'] = list_old_price



print(dict)