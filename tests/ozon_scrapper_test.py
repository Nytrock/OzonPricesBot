import asyncio

from exernal_services.ozon_scrapper import get_product_data_from_ozon, get_products_by_search

async def main():
    print(await get_products_by_search('конструктор', 1))
    print(await get_products_by_search('конструктор', 2))
    print(await get_products_by_search('конструктор', 10))
    print(await get_products_by_search('цилиндр', 1))
    print(await get_products_by_search('цилиндр', 2))
    print(await get_products_by_search('цилиндр', 10))
    print(await get_products_by_search('ламинария', 1))
    print(await get_products_by_search('ламинария', 2))
    print(await get_products_by_search('ламинария', 10))


asyncio.run(main())
