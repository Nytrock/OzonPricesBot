import asyncio

from exernal_services.ozon_scrapper import get_product_data_from_ozon, get_products_by_search

async def main():
    print(await get_product_data_from_ozon(1505354070))
    print(await get_product_data_from_ozon(1580742819))
    print(await get_product_data_from_ozon(1580632102))


asyncio.run(main())
