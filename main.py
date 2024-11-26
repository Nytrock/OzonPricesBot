import asyncio

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram_dialog import Dialog, setup_dialogs

from config_data.config import Config, load_config
from database.methods import create_tables
from handlers import registration, admin_panel, main_menu, favorites, products, settings
from lexicon.lexicon import LEXICON
from middlewares.i18n import TranslatorMiddleware
from middlewares.user_role import UserRoleMiddleware

dialog = Dialog(
    main_menu.window
)


async def main():
    config: Config = load_config()
    storage = MemoryStorage()

    bot = Bot(token=config.tg_bot.token)
    dp = Dispatcher(storage=storage)

    await create_tables()

    dp['translations'] = LEXICON

    dp.include_router(registration.router)
    dp.include_router(main_menu.router)
    dp.include_router(admin_panel.router)
    dp.include_router(settings.router)
    dp.include_router(favorites.router)
    dp.include_router(products.router)

    dp.update.outer_middleware(UserRoleMiddleware())
    dp.update.middleware(TranslatorMiddleware())

    dp.include_router(dialog)
    setup_dialogs(dp)

    await bot.delete_webhook()
    await dp.start_polling(bot)


asyncio.run(main())
