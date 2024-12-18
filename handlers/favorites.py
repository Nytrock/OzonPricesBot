import math
from typing import Any

from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Button

from database.methods import get_user_favorites, get_product_info, remove_favorite
from handlers.products import add_product_data_to_dialog
from states.states import ProductsDialogStates

FAVORITES_ROWS_COUNT = 5


# Получение избранных товаров пользователя
async def get_favorites(**kwargs) -> dict[str, Any]:
    manager = kwargs['dialog_manager']
    user_id = manager.event.from_user.id

    favorites = await get_user_favorites(user_id)
    if not manager.dialog_data.get('page_num'):
        manager.dialog_data['page_num'] = 1

    manager.dialog_data['max_pages'] = math.ceil(len(favorites) / FAVORITES_ROWS_COUNT)
    if manager.dialog_data['page_num'] > manager.dialog_data['max_pages']:
        manager.dialog_data['page_num'] = manager.dialog_data['max_pages']

    page_num = manager.dialog_data['page_num']
    favorites = favorites[(page_num - 1) * FAVORITES_ROWS_COUNT:page_num * FAVORITES_ROWS_COUNT]
    return {'favorites': favorites}


# Переключение на прошлую страницу избранного
async def previous_favorites(_0: CallbackQuery, _1: Button, manager: DialogManager) -> None:
    manager.dialog_data['page_num'] -= 1


# Переключение на следующую страницу избранного
async def next_favorites(_0: CallbackQuery, _1: Button, manager: DialogManager) -> None:
    manager.dialog_data['page_num'] += 1


# Открытие избранного товара
async def open_favorite_product(callback: CallbackQuery, _: Button, manager: DialogManager) -> None:
    product_id = int(callback.item_id)
    product_data = await get_product_info(product_id)

    await add_product_data_to_dialog(callback.from_user.id, product_data, manager)
    await manager.start(ProductsDialogStates.product_detail, data=manager.dialog_data)


# Удаление избранного товара
async def remove_favorite_product(callback: CallbackQuery, _: Button, manager: DialogManager) -> None:
    product_id = int(callback.item_id)
    user_id = manager.event.from_user.id
    await remove_favorite(user_id, product_id)
