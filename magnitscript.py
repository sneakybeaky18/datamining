from bs4 import BeautifulSoup
import requests
from urllib.parse import urlparse
from pymongo import MongoClient
import re

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
    el_filter_1 = el.text.replace('\n','')
    el_filter_2 = el_filter_1.replace('%','')
    el_filter_3 = el_filter_2.replace('−', '')
    list_new_price.append(int(el_filter_3)/100)
dict['new_price'] = list_new_price


list_old_price = [] #получаем старую цену
for el in soup.find_all('div', attrs={'class': 'label__price_old'}):
    list_old_price.append(int(el.text.replace('\n',''))/100)
dict['old_price'] = list_old_price


url = 'https://magnit.ru/promo/?geo=moskva' #получаем ссылки, тайм код 1:19:43
list_of_links = [] #получаем ссылку
catalog = soup.find('div', attrs={'class': "сatalogue__main"})
products = catalog.findChildren('a', attrs={'class': 'card-sale'})
for product in products:
    if len(product.attrs.get('class')) > 2 or product.attrs.get('href')[0] != '/':
        continue
    product_url = product.attrs.get("href")
    list_of_links.append(product_url)
dict['url'] = list_of_links

print(dict)