from bs4 import BeautifulSoup
import requests
from urllib.parse import urlparse
from pymongo import MongoClient

headers = {
    'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:81.0) Gecko/20100101 Firefox/81.0",
}
params = {
    'geo': 'moskva',
}

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

