import html
import json
import textwrap

from bs4 import BeautifulSoup
from typing import Any
from curl_cffi import requests
from utils.url_parser import get_product_id_from_inner_url

PRODUCT_URL = 'https://www.ozon.ru/product'
SEARCH_URL = 'https://www.ozon.ru/api/entrypoint-api.bx/page/json/v2?url=/search/?page={page_index}&text={text}'
SEARCH_URL_SPARE = 'https://www.ozon.ru/api/entrypoint-api.bx/page/json/v2?url=/search/?page_index={page_index}&text={text}'
SEARCH_RESULTS_COUNT = 8

PRICE_SYMBOLS = [' ', '₽']


async def get_page_soup(url: str) -> BeautifulSoup:
    session = requests.Session()
    response = session.get(url)
    soup = BeautifulSoup(response.text, 'lxml')
    return soup


async def get_product_prices_from_soup(product_soup: BeautifulSoup) -> dict[str, int]:
    result = {'regular_price': -1, 'card_price': -1}
    price_div = product_soup.find(attrs={'data-widget' : 'webPrice'})
    if price_div is None:
        return {}

    out_of_stock_div = product_soup.find(attrs={'data-widget' : 'webOutOfStock'})
    result['in_stock'] = out_of_stock_div is None

    prices = price_div.get_text()
    for text in prices.split(' '):
        if text == '':
            continue

        for symbol in PRICE_SYMBOLS:
            text = text.replace(symbol, '')

        if text.isdigit():
            if result['card_price'] == -1:
                result['card_price'] = int(text)
                if 'c Ozon Картой' not in prices:
                    result['regular_price'] = int(text)
            elif result['regular_price'] == -1:
                result['regular_price'] = int(text)
                break

    return result


async def get_product_data_from_ozon(product_id: int) -> dict[str, Any]:
    result = {'id': product_id}
    product_soup = await get_page_soup(f'{PRODUCT_URL}/{product_id}/?oos_search=false')
    result |= await get_product_prices_from_soup(product_soup)

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

    result['title'] = html.unescape(product_info['name'])
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

async def get_products_by_search(text: str, page_index=1) -> list[dict[str, Any]]:
    url = SEARCH_URL.format(text=text, page_index=page_index)
    data = await get_search_data(url)
    if not data:
        url = SEARCH_URL_SPARE.format(text=text, page_index=page_index)
        data = await get_search_data(url)

    result = []
    if not data:
        return result

    for item in data['items']:
        item_data = {
            'id': get_product_id_from_inner_url(item['action']['link'])
        }

        for state in item['mainState']:
            if state['atom'].get('textAtom'):
                if state['atom']['textAtom']['textStyle'] == 'tsBodyL':
                    item_data['title'] = state['atom']['textAtom']['text']
                    break
        item_data['title'] = html.unescape(item_data['title'])
        result.append(item_data)
    return result


async def get_search_data(url: str) -> dict[str, Any]:
    session = requests.Session()
    response = session.get(url)
    data = json.loads(response.text)['widgetStates']

    result = {}
    for key in data.keys():
        if key.startswith('searchResultsV2') and data[key] != '{}':
            result = json.loads(data[key])
    return result
