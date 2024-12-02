import asyncio

from exernal_services.ozon_scrapper import get_product_data_from_ozon

async def main():
    for i in range(100000000, 9999999999):
        print(await get_product_data_from_ozon(i))

asyncio.run(main())
