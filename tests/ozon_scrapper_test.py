import asyncio

from exernal_services.ozon_scrapper import get_product_data_from_ozon, get_products_by_search

async def main():
    print(await get_product_data_from_ozon(1667404254))
    print(await get_product_data_from_ozon(1646643316))
    print(await get_product_data_from_ozon(909110814))
    print(await get_product_data_from_ozon(285813483))
    print(await get_product_data_from_ozon(1))
    print(await get_product_data_from_ozon(935358735))
    print(await get_product_data_from_ozon(9872234))

    for i in range(1, 10):
        print(await get_products_by_search('ламинария', i))
    print(await get_products_by_search('ламинария', 10000))


asyncio.run(main())
