import json
from pprint import pprint

from bs4 import BeautifulSoup
from typing import Any
from curl_cffi import requests

from utils.url_parser import get_product_id_from_inner_url

PRODUCT_URL = 'https://www.ozon.ru/product'
SEARCH_URL = 'https://www.ozon.ru/search/?text='
SEARCH_RESULTS_COUNT = 8

PRICE_SYMBOLS = [' ', '₽']


def get_page_soup(url: str) -> BeautifulSoup:
    session = requests.Session()
    response = session.get(url)
    soup = BeautifulSoup(response.text, 'lxml')
    return soup


def get_product_prices_by_id(product_id: int) -> dict[str, int]:
    product_soup = get_page_soup(f'{PRODUCT_URL}/{product_id}/?oos_search=false')
    return get_product_prices_from_soup(product_soup)


def get_product_prices_from_soup(product_soup: BeautifulSoup) -> dict[str, int]:
    result = {'regular_price': -1, 'card_price': -1}
    price_div = product_soup.find(attrs={'data-widget' : 'webPrice'})
    if price_div is None:
        result['is_not_exists'] = True
        return result

    out_of_stock_div = product_soup.find(attrs={'data-widget' : 'webOutOfStock'})
    if out_of_stock_div is not None:
        return result

    for text in price_div.get_text().split(' '):
        if text == '':
            continue

        for symbol in PRICE_SYMBOLS:
            text = text.replace(symbol, '')

        if text.isdigit():
            if result['regular_price'] == -1:
                result['regular_price'] = int(text)
            elif result['card_price'] == -1:
                result['card_price'] = int(text)
                break

    return result

def get_product_info_by_id(product_id: int) -> dict[str, Any]:
    result = {}
    product_soup = get_page_soup(f'{PRODUCT_URL}/{product_id}/?oos_search=false')
    result |= get_product_prices_from_soup(product_soup)

    if result.get('is_not_exists'):
        result = {'regular_price': -1, 'card_price': -1, 'title': '', 'brand': '',
                  'rating': 0, 'rating_count': 0, 'image': '', 'description': '', 'variations': []}
        return result

    info_div = product_soup.find('script', attrs={'type': 'application/ld+json'})
    product_info = json.loads(info_div.text)

    if product_info.get('aggregateRating') is None:
        result['rating'] = 0
        result['rating_count'] = 0
    else:
        result['rating'] = product_info['aggregateRating']['ratingValue']
        result['rating_count'] = product_info['aggregateRating']['reviewCount']

    result['brand'] = product_info['brand']
    result['title'] = product_info['name']
    result['image'] = product_info['image']
    result['description'] = product_info['description']

    variants_div = product_soup.find(id='state-webAspects-3529295-default-1')
    if variants_div is None:
        result['variants'] = []
        return result

    result['variants'] = set()
    variants_data = json.loads(variants_div['data-state'])
    for aspect in variants_data['aspects']:
        for variant in aspect['variants']:
            variation_id = get_product_id_from_inner_url(variant['link'])
            if variation_id != product_id:
                result['variants'].add(variation_id)
    result['variants'] = list(result['variants'])

    return result

def get_products_by_search(text: str) -> list[int]:
    search_soup = get_page_soup(f'{SEARCH_URL}{text}')
    products_div = search_soup.find(attrs={'data-widget': 'searchResultsV2'})

    result = []
    for i in range(SEARCH_RESULTS_COUNT):
        product = products_div.find(attrs={'data-index': str(i)})
        product_link = product.a['href']
        result.append(get_product_id_from_inner_url(product_link))
    return result
