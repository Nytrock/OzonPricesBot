import asyncio
import platform

from exernal_services.ozon_scrapper import get_product_data_from_ozon


# Тестирования парсера озона
async def main():
    print(await get_product_data_from_ozon(1667404254))
    print(await get_product_data_from_ozon(1646643316))
    print(await get_product_data_from_ozon(909110814))
    print(await get_product_data_from_ozon(285813483))
    print(await get_product_data_from_ozon(1))
    print(await get_product_data_from_ozon(935358735))
    print(await get_product_data_from_ozon(9872234))


if __name__ == "__main__":
    if platform.system() == 'Windows':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main())
