import asyncio

from exernal_services.ozon_scrapper import get_product_info_by_id, get_products_by_search

async def main():
    print(await get_product_info_by_id(1667404254))
    print(await get_product_info_by_id(1646643316))
    print(await get_product_info_by_id(909110814))
    print(await get_product_info_by_id(285813483))
    print(await get_product_info_by_id(1))
    print(await get_product_info_by_id(935358735))
    print(await get_product_info_by_id(9872234))

    for i in range(1, 10):
        print(await get_products_by_search('ламинария', i))


asyncio.run(main())
