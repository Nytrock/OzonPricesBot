import json

from bs4 import BeautifulSoup
from typing import Any
from curl_cffi import requests

from utils.url_parser import get_product_id_from_inner_url

PRODUCT_URL = 'https://www.ozon.ru/product'
SEARCH_URL = 'https://www.ozon.ru/search/?text='
SEARCH_RESULTS_COUNT = 8

PRICE_SYMBOLS = [' ', '₽']
REQUEST_HEADERS = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-encoding': 'gzip, deflate, br, zstd',
    'accept-language': 'ru,en-US;q=0.9,en;q=0.8,zh-CN;q=0.7,zh;q=0.6',
    'cookie': '__Secure-ab-group=95; __Secure-ext_xcid=52e9d0903b5ee0eb6bdc729106a90dc9; __Secure-ETC=5f256a2a504be30a16f9d821cde3f629; is_cookies_accepted=1; TS015d2969=0187c00a189d53723d1f461a715f57ba9d34a59dce3a909f481ae818823f6d3c78acf753e6a847fcb3653b6c084584d9306b84784b; xcid=842eee79020c27c7b7908e1ae9ad99cc; ADDRESSBOOKBAR_WEB_CLARIFICATION=1731152158; rfuid=NjkyNDcyNDUyLDEyNC4wNDM0NzUyNzUxNjA3NCwxMDI4MjM3MjIzLC0xLC0xOTAwMDQ5ODE1LFczc2libUZ0WlNJNklrTm9jbTl0WlNCUVJFWWdVR3gxWjJsdUlpd2laR1Z6WTNKcGNIUnBiMjRpT2lKUWIzSjBZV0pzWlNCRWIyTjFiV1Z1ZENCR2IzSnRZWFFpTENKdGFXMWxWSGx3WlhNaU9sdDdJblI1Y0dVaU9pSmhjSEJzYVdOaGRHbHZiaTk0TFdkdmIyZHNaUzFqYUhKdmJXVXRjR1JtSWl3aWMzVm1abWw0WlhNaU9pSndaR1lpZlYxOUxIc2libUZ0WlNJNklrTm9jbTl0WlNCUVJFWWdWbWxsZDJWeUlpd2laR1Z6WTNKcGNIUnBiMjRpT2lJaUxDSnRhVzFsVkhsd1pYTWlPbHQ3SW5SNWNHVWlPaUpoY0hCc2FXTmhkR2x2Ymk5d1pHWWlMQ0p6ZFdabWFYaGxjeUk2SW5Ca1ppSjlYWDFkLFd5SnlkU0pkLDAsMSwwLDI0LDIzNzQxNTkzMCw4LDIyNzEyNjUyMCwwLDEsMCwtNDkxMjc1NTIzLFIyOXZaMnhsSUVsdVl5NGdUbVYwYzJOaGNHVWdSMlZqYTI4Z1YybHVNeklnTlM0d0lDaFhhVzVrYjNkeklFNVVJREV3TGpBN0lGZHBialkwT3lCNE5qUXBJRUZ3Y0d4bFYyVmlTMmwwTHpVek55NHpOaUFvUzBoVVRVd3NJR3hwYTJVZ1IyVmphMjhwSUVOb2NtOXRaUzh4TXpBdU1DNHdMakFnVTJGbVlYSnBMelV6Tnk0ek5pQXlNREF6TURFd055Qk5iM3BwYkd4aCxleUpqYUhKdmJXVWlPbnNpWVhCd0lqcDdJbWx6U1c1emRHRnNiR1ZrSWpwbVlXeHpaU3dpU1c1emRHRnNiRk4wWVhSbElqcDdJa1JKVTBGQ1RFVkVJam9pWkdsellXSnNaV1FpTENKSlRsTlVRVXhNUlVRaU9pSnBibk4wWVd4c1pXUWlMQ0pPVDFSZlNVNVRWRUZNVEVWRUlqb2libTkwWDJsdWMzUmhiR3hsWkNKOUxDSlNkVzV1YVc1blUzUmhkR1VpT25zaVEwRk9UazlVWDFKVlRpSTZJbU5oYm01dmRGOXlkVzRpTENKU1JVRkVXVjlVVDE5U1ZVNGlPaUp5WldGa2VWOTBiMTl5ZFc0aUxDSlNWVTVPU1U1SElqb2ljblZ1Ym1sdVp5SjlmWDE5LDY1LC0xMjg1NTUxMywxLDEsLTEsMTY5OTk1NDg4NywxNjk5OTU0ODg3LDMzNjAwNzkzMywxNg==; __Secure-access-token=6.0.mDk5XOs8RpiqQ7BJwSx0vg.95.AXwW-TfzSEuWgvm-WivUTOPSCZgpMKky_SJb_7UspSL_Uik6gsRV-X-i5_sivm867A..20241109162907.ApgyYk5NwiQLAMmZmbxX7sfaH6TdwVWwxrr14umeMls.1d7845304134865fd; __Secure-refresh-token=6.0.mDk5XOs8RpiqQ7BJwSx0vg.95.AXwW-TfzSEuWgvm-WivUTOPSCZgpMKky_SJb_7UspSL_Uik6gsRV-X-i5_sivm867A..20241109162907.dbveyPw_86XbbMjttfuenAicyOqpZw2xJNDOX4IuzCY.192e572a8a8dd7393; __Secure-user-id=0; is_adult_confirmed=; is_alco_adult_confirmed=; abt_data=7.rocgYiqtLkxie2kCO815PsgxvDVH2_xruOWApxxB2U778VUBl1pyHqGkkiVol6PJxwNnRRzdkvr6jcfQ4dRlXxvRDHhI29MlUzBf2g4-H_HZiJUrWQXVKn66WidIRT75X_dMb67W7110PV-NEg3BE0zV8iUjWeAxPUk4K3Ufbo9z4kbxZFwo_WosMF63bZq2AztJw-EaIcy9hAg0MEA2OLZC7AcavXZ4uACB0M8qQaDuJ46cYTDxn_CTCaoFPMEnGGJhVF_BKnCcJCrUVKtIBK-N6Gsy8Br03T_RU3hPu8dUfvBVa1J1Sd4xsRWg1OhTJEZpyGn-JDh4uLHBSJ9CMG_CaOaq2vLX_yplg37eneCwZQVAVHUnkCe0luMTeysc56q3mEa7e-laxHsrfRbtD4dNrX9-5H834ex4nZF1e2E5PEgXWz4BQ0n6ys8xoGxdUc0czgIZrLd7X6BIZCnS7AX8XuK5RhBtdG4aStCPbE34Ipa9JaHC8Z7nYAkgJ1weR5sm78DxJY30k4094A; guest=true; TS01f9fe57=0187c00a187ffbf0c23b2b6936993c25f6a17ca4aa99948dda65a3debb7cbdfb164d1e8756168c0ad6928f172ded5dd82c6e7ece0d; TS013595b9=0187c00a184f976a358a25915503d156936dc455aa0d552a288b3532ff136683ad3639d98d34c322fab51fd7facdd53b66d77be150',
    'priority': 'u=0, i',
    'pragma': 'no-cache',
    'sec-ch-ua': '"Chromium";v="130", "Google Chrome";v="130", "Not?A_Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'none',
    'sec-fetch-user': '?1',
    'service-worker-navigation-preload': 'true',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36'}


def get_page_soup(url: str) -> BeautifulSoup:
    session = requests.Session()
    response = session.get(url, headers=REQUEST_HEADERS)
    soup = BeautifulSoup(response.text, 'lxml')
    return soup


def get_product_prices_by_id(product_id: int) -> dict[str, int]:
    product_soup = get_page_soup(f'{PRODUCT_URL}/{product_id}/?oos_search=false')
    return get_product_prices_from_soup(product_soup)


def get_product_prices_from_soup(product_soup: BeautifulSoup) -> dict[str, int]:
    result = {'regular_price': -1, 'card_price': -1}
    price_div = product_soup.find(attrs={'data-widget' : 'webPrice'})
    if price_div is None:
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

    if result['regular_price'] == -1 and result['card_price'] == -1:
        result.update({'title': '', 'rating': 0, 'image': '', 'variations': []})
        return result

    title_div = product_soup.find(attrs={'data-widget': 'webProductHeading'})
    result['title'] = title_div.get_text().strip()

    rating_div = product_soup.find(attrs={'data-widget': 'webSingleProductScore'})
    if rating_div is None or '•' not in rating_div.get_text():
        result['rating'] = 0
    else:
        result['rating'] = float(rating_div.get_text().split('•')[0])


    image = product_soup.head.find('link', attrs={'as': 'image'})
    result['image'] = image['href']

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
