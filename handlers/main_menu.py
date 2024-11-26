from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery
from aiogram_dialog import Window, DialogManager, StartMode
from aiogram_dialog.widgets.kbd import Row, Button
from aiogram_dialog.widgets.text import Format

from filters.user_role import IsUserRegistered
from utils.dialog import get_dialog_i18n
from states.states import FSMDialog

router = Router()
router.message.filter(IsUserRegistered())


async def to_settings(callback: CallbackQuery, button: Button, manager: DialogManager):
    await manager.switch_to(FSMDialog.settings)


async def to_favorites(callback: CallbackQuery, button: Button, manager: DialogManager):
    await manager.switch_to(FSMDialog.favorites)


async def to_admin_users(callback: CallbackQuery, button: Button, manager: DialogManager):
    await manager.switch_to(FSMDialog.admin_users)


async def to_admin_products(callback: CallbackQuery, button: Button, manager: DialogManager):
    await manager.switch_to(FSMDialog.admin_products)

window = Window(
    Format(get_dialog_i18n('main_menu')),
    Button(Format(get_dialog_i18n('main_menu_products')), id='products'),
    Row(
        Button(
            Format(get_dialog_i18n('main_menu_settings')),
            id='settings',
            on_click=to_settings
        ),
        Button(
            Format(get_dialog_i18n('main_menu_favorites')),
            id='favorites',
            on_click=to_favorites
        ),
    ),
    Row(
        Button(
            Format(get_dialog_i18n('main_menu_admin_users')),
            id='admin_users',
            on_click=to_admin_users,
            when='middleware_data[user_is_admin]'
        ),
        Button(
            Format(get_dialog_i18n('main_menu_admin_products')),
            id='admin_products',
            on_click=to_admin_products,
            when='middleware_data[user_is_admin]'
        ),
    ),
    state=FSMDialog.main_menu,
)


@router.message(CommandStart())
async def start_main_menu(message: Message, dialog_manager: DialogManager):
    await dialog_manager.start(FSMDialog.main_menu, mode=StartMode.RESET_STACK)
