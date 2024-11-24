import asyncio

from aiogram import Bot, Dispatcher
from config_data.config import Config, load_config
from database.methods import create_tables


async def main():
    config: Config = load_config()

    bot = Bot(token=config.tg_bot.token)
    dp = Dispatcher()

    await create_tables()
    await dp.start_polling(bot)


asyncio.run(main())
