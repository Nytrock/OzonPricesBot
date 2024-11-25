import asyncio

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from config_data.config import Config, load_config
from database.methods import create_tables
from handlers import registration, admin_panel, commands, favorites, products, settings
from lexicon.lexicon import LEXICON
from middlewares.i18n import TranslatorMiddleware
from middlewares.user_role import UserRoleMiddleware


async def main():
    config: Config = load_config()
    storage = MemoryStorage()

    bot = Bot(token=config.tg_bot.token)
    dp = Dispatcher(storage=storage)

    await create_tables()

    dp.include_router(registration.router)
    dp.include_router(admin_panel.router)
    dp.include_router(commands.router)
    dp.include_router(favorites.router)
    dp.include_router(settings.router)
    dp.include_router(products.router)

    dp.update.outer_middleware(UserRoleMiddleware)

    dp['translations'] = LEXICON

    await dp.start_polling(bot)


asyncio.run(main())
