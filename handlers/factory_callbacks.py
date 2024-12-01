from aiogram import Router
from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager, StartMode

from callback_factory.callback_factory import ProductCallbackFactory
from database.methods import get_product_info
from filters.registration import IsUserRegistered
from handlers.products import add_product_data_to_dialog
from states.states import MainMenuDialogStates, ProductsDialogStates

router = Router()
router.message.filter(IsUserRegistered())

@router.callback_query(ProductCallbackFactory.filter())
async def notification_open(callback: CallbackQuery, callback_data: ProductCallbackFactory, dialog_manager: DialogManager):
    await dialog_manager.start(MainMenuDialogStates.main_menu, mode=StartMode.RESET_STACK)

    product_data = await get_product_info(callback_data.product_id)
    await add_product_data_to_dialog(callback.from_user.id, product_data, dialog_manager)
    await dialog_manager.start(ProductsDialogStates.product_detail, data=dialog_manager.dialog_data)
