from aiogram.types import Message
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.input import MessageInput

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
        await message.answer('Тут типа поиск')
    else:
        product_data = await get_product_info(product_id)
        if product_data == {}:
            await message.answer(manager.middleware_data['i18n']['product_search_id_error'])
        else:
            manager.dialog_data['product'] = product_data
            await manager.switch_to(ProductsDialogStates.product_detail)
