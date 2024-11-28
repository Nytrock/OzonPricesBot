import json
import re
import textwrap
from lib2to3.fixes.fix_input import context
from pprint import pprint

from bs4 import BeautifulSoup
from typing import Any
from curl_cffi import requests
from sqlalchemy import result_tuple

from utils.dialog import Translate
from utils.url_parser import get_product_id_from_inner_url

PRODUCT_URL = 'https://www.ozon.ru/product'
SEARCH_URL = 'https://www.ozon.ru/api/entrypoint-api.bx/page/json/v2?url=/search/?Flayout_container=categorySearchMegapagination&layout_page_index={page_index}&page={page_index}&text={text}'
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
        return {}

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

async def get_product_data_from_ozon(product_id: int) -> dict[str, Any]:
    result = {'id': product_id}
    product_soup = get_page_soup(f'{PRODUCT_URL}/{product_id}/?oos_search=false')
    result |= get_product_prices_from_soup(product_soup)

    if result.get('regular_price') is None:
        return {}

    info_div = product_soup.find('script', attrs={'type': 'application/ld+json'})
    product_info = json.loads(info_div.text)

    if product_info.get('aggregateRating') is None:
        result['rating'] = 0
        result['rating_count'] = 0
    else:
        result['rating'] = float(product_info['aggregateRating']['ratingValue'])
        result['rating_count'] = int(product_info['aggregateRating']['reviewCount'])

    result['title'] = product_info['name']
    result['image'] = product_info['image']
    result['description'] = textwrap.shorten(product_info['description'], width=200, placeholder='...')

    seller_div = product_soup.find(id=lambda value: value and value.startswith('state-webStickyProducts-'))
    result['seller'] = json.loads(seller_div['data-state'])['seller']['name']

    variants_div = product_soup.find(id=lambda value: value and value.startswith('state-webAspects-'))
    if variants_div is None:
        result['variations'] = set()
        return result

    result['variations'] = set()
    variants_data = json.loads(variants_div['data-state'])
    for aspect in variants_data['aspects']:
        for variant in aspect['variants']:
            variation_id = get_product_id_from_inner_url(variant['link'])
            if variation_id != product_id:
                result['variations'].add(variation_id)
    result['variations'] = list(result['variations'])

    return result

async def get_products_by_search(text: str, page_index=1) -> list[int]:
    url = SEARCH_URL.format(text=text, page_index=page_index)
    session = requests.Session()
    response = session.get(url)
    data = json.loads(response.text)['widgetStates']

    is_data_find = False
    for key in data.keys():
        if key.startswith('searchResultsV2') and data[key] != '{}':
            data = json.loads(data[key])
            is_data_find = True
            break

    result = []
    if not is_data_find:
        return result

    for item in data['items']:
        item_id = item['multiButton']['ozonButton']['addToCartButtonWithQuantity']['action']['id']
        result.append(int(item_id))
    return result
