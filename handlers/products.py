from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Button

from states.states import ProductsDialogStates


async def to_product_search(_0: CallbackQuery, _1: Button, manager: DialogManager):
    await manager.start(ProductsDialogStates.product_search)
