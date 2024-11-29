from math import trunc
from typing import Any

from aiogram.types import Message, CallbackQuery
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Button

from database.methods import get_product_info, is_favorite_exists, change_favorite
from enums.user_data import UserShowVariations
from exernal_services.ozon_scrapper import get_products_by_search
from states.states import ProductsDialogStates
from utils.url_parser import get_product_id_from_url


async def search_product(message: Message, _: MessageInput, manager: DialogManager):
    text = message.text
    if text.isdigit():
        product_id = int(text)
    else:
        product_id = get_product_id_from_url(text)

    if product_id == -1:
        manager.dialog_data['search_query'] = text
        manager.dialog_data['search_page'] = 1
        manager.dialog_data['search_data'] = []
        await get_search_page_data(manager)
        await manager.switch_to(ProductsDialogStates.product_search)
    else:
        product_data = await get_product_info(product_id)
        if product_data == {}:
            await message.answer(manager.middleware_data['i18n']['product_id_error'])
        else:
            await finalize_product_data(product_data, manager)
            await add_product_data_to_manager(message.from_user.id, product_data, manager)
            await manager.switch_to(ProductsDialogStates.product_detail)


async def change_variations_mode(_0: CallbackQuery, _1: Button, manager: DialogManager):
    manager.dialog_data['variations_mode'] = not manager.dialog_data['variations_mode']


async def change_product(callback: CallbackQuery, _: Button, manager: DialogManager):
    product_id = int(callback.item_id)
    product_data = await get_product_info(product_id)
    await finalize_product_data(product_data, manager)
    await add_product_data_to_manager(callback.from_user.id, product_data, manager)
    await manager.switch_to(ProductsDialogStates.product_detail)


async def finalize_product_data(product_data: dict[str, Any], manager: DialogManager) -> None:
    user_have_card = manager.middleware_data['user_have_card']
    user_show_variations = manager.middleware_data['user_show_variations']

    limit_variations = []
    for variation in product_data['variations']:
        if user_show_variations == UserShowVariations.only_cheaper.value:
            if not user_have_card and variation['regular_price'] < product_data['regular_price']:
                limit_variations.append(variation)
            if user_have_card and variation['card_price'] < product_data['card_price']:
                limit_variations.append(variation)
        elif user_show_variations == UserShowVariations.all.value:
            limit_variations.append(variation)

    product_data['variations'] = limit_variations


async def add_product_data_to_manager(user_id: int, product_data: dict[str, Any], manager: DialogManager) -> None:
    manager.dialog_data['product'] = product_data
    manager.dialog_data['variations_mode'] = False
    manager.dialog_data['have_variations'] = bool(product_data['variations'])
    manager.dialog_data['into_favorites'] = await is_favorite_exists(user_id, product_data['id'])


async def next_search_page(_0: CallbackQuery, _1: Button, manager: DialogManager):
    manager.dialog_data['search_page'] += 1
    await get_search_page_data(manager)


async def previous_search_page(_0: CallbackQuery, _1: Button, manager: DialogManager):
    manager.dialog_data['search_page'] -= 1
    await get_search_page_data(manager)


async def get_search_page_data(manager: DialogManager):
    page_num = manager.dialog_data['search_page']
    query = manager.dialog_data['search_query']

    if page_num > len(manager.dialog_data['search_data']):
        products = await get_products_by_search(query, page_num)
        manager.dialog_data['search_data'].append(products)
        manager.dialog_data['search_products'] = products
        manager.dialog_data['have_search_result'] = bool(products)
    else:
        manager.dialog_data['search_products'] = manager.dialog_data['search_data'][page_num - 1]
        manager.dialog_data['have_search_result'] = True


async def change_product_favorite(callback: CallbackQuery, _: Button, manager: DialogManager) -> None:
    product_id = manager.dialog_data['product']['id']
    user_id = callback.from_user.id

    favorite_created = await change_favorite(user_id, product_id)
    manager.dialog_data['into_favorites'] = favorite_created
