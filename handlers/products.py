from aiogram.types import Message, CallbackQuery
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Button

from database.methods import get_product_info
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
        # получение информации для поискового вывода
        await manager.switch_to(ProductsDialogStates.product_search)
    else:
        product_data = await get_product_info(product_id)
        if product_data == {}:
            await message.answer(manager.middleware_data['i18n']['product_id_error'])
        else:
            manager.dialog_data['product'] = product_data
            manager.dialog_data['variations_mode'] = False
            await manager.switch_to(ProductsDialogStates.product_detail)


async def change_variations_mode(_0: CallbackQuery, _1: Button, manager: DialogManager):
    manager.dialog_data['variations_mode'] = not manager.dialog_data['variations_mode']


async def change_product(callback: CallbackQuery, _: Button, manager: DialogManager):
    product_id = callback.item_id
    product_data = await get_product_info(product_id)

    manager.dialog_data['product'] = product_data
    manager.dialog_data['variations_mode'] = False
