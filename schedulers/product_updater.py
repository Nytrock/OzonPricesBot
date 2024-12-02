from typing import Any

from aiogram import Bot
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger
from pyrogram import Client

from config_data.config import load_config
from database.methods import get_product_prices, create_product_price, get_all_products_with_users_favorite, \
    update_product
from database.models import Product, Price
from enums.user_data import UserSendNotifications
from exernal_services.ozon_scrapper import get_product_data_from_ozon
from keyboards.keyboard_utils import create_notification_kb
from lexicon.lexicon import LEXICON


def setup_scheduler(bot: Bot) -> None:
    scheduler = AsyncIOScheduler()
    scheduler.add_job(update_prices, IntervalTrigger(hours=6), args=(bot,))
    scheduler.start()


async def update_prices(bot: Bot) -> None:
    products = await get_all_products_with_users_favorite()
    if len(products) == 0:
        return

    for product in products:
        prices = await get_product_prices(product.id)
        last_price = prices[-1]

        price_data = await get_product_data_from_ozon(product.id)
        await update_product(price_data)
        if price_data['regular_price'] != last_price.regular_price or price_data['card_price'] != last_price.card_price:
            price_data['id'] = product.id
            await create_product_price(price_data)
            await notification_users(product, last_price, price_data, bot)


async def notification_users(product: Product, old_price: Price, new_price: dict[str, Any], bot: Bot):
    for user in product.users_favorite:
        if user.have_card:
            old_price_num = old_price.card_price
            new_price_num = new_price['card_price']
        else:
            old_price_num = old_price.regular_price
            new_price_num = new_price['regular_price']

        if old_price_num == new_price_num:
            continue

        user_notifications_mode = UserSendNotifications(user.send_notifications)
        send_user_notification = True

        if user_notifications_mode == UserSendNotifications.no:
            send_user_notification = False
        elif user_notifications_mode == UserSendNotifications.only_lowering and old_price_num < new_price_num:
            send_user_notification = False

        if not send_user_notification:
            continue

        config = load_config().tg_api
        async with Client(config.username, api_id=config.api_id, api_hash=config.api_hash) as ubot:
            user_data = await ubot.get_users(user.id)
            language_code = user_data.language_code
            if language_code not in LEXICON.keys():
                language_code = LEXICON['default']

        message_text = LEXICON[language_code]['notification'].format(
            product=product.title,
            old_price=old_price_num,
            new_price=new_price_num
        )
        await bot.send_message(
            user.id,
            text=message_text,
            reply_markup=create_notification_kb(product.id, LEXICON[language_code])
        )
