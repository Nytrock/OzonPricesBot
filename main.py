import asyncio

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram_dialog import setup_dialogs

from config_data.config import Config, load_config
from database.database import create_tables
from dialogs import main_menu, admin, settings, favorites, products
from handlers import registration, other_commands
from lexicon.lexicon import LEXICON
from middlewares.i18n import TranslatorMiddleware
from middlewares.user_data import UserDataMiddleware


async def main():
    config: Config = load_config()
    storage = MemoryStorage()

    bot = Bot(token=config.tg_bot.token)
    dp = Dispatcher(storage=storage)

    await create_tables()

    dp['translations'] = LEXICON

    dp.include_router(registration.router)
    dp.include_router(other_commands.router)

    dp.update.outer_middleware(UserDataMiddleware())
    dp.update.middleware(TranslatorMiddleware())

    dp.include_router(main_menu.dialog)
    dp.include_router(admin.dialog)
    dp.include_router(settings.dialog)
    dp.include_router(favorites.dialog)
    dp.include_router(products.dialog)
    setup_dialogs(dp)

    await bot.delete_webhook()
    await dp.start_polling(bot)


asyncio.run(main())
