import asyncio
import platform

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram_dialog import setup_dialogs

from config_data.config import Config, load_config
from database.database import create_tables
from dialogs import main_menu, admin, settings, favorites, products
from dialogs.message_manager import CustomMessageManager
from handlers import registration, other_commands, factory_callbacks
from lexicon.lexicon import LEXICON
from middlewares.i18n import TranslatorMiddleware
from middlewares.user_data import UserDataMiddleware
from schedulers import product_updater


# Запуск приложения
async def main():
    config: Config = load_config()
    storage = MemoryStorage()

    bot = Bot(
        token=config.tg_bot.token,
    )
    dp = Dispatcher(
        storage=storage,
        translations=LEXICON
    )

    await create_tables()

    # Добавление роутеров
    dp.include_router(registration.router)
    dp.include_router(other_commands.router)
    dp.include_router(factory_callbacks.router)

    # Добавление миддлварей
    dp.update.outer_middleware(UserDataMiddleware())
    dp.update.middleware(TranslatorMiddleware())

    # Добавление диалогов
    dp.include_router(main_menu.dialog)
    dp.include_router(admin.dialog)
    dp.include_router(settings.dialog)
    dp.include_router(favorites.dialog)
    dp.include_router(products.dialog)

    setup_dialogs(dp, message_manager=CustomMessageManager())
    product_updater.setup_scheduler(bot)

    await bot.delete_webhook()
    await dp.start_polling(bot)

if __name__ == "__main__":
    if platform.system() == 'Windows':
            asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main())
