from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Button


async def go_back(callback: CallbackQuery, button: Button, manager: DialogManager):
    await manager.back()


async def go_next(callback: CallbackQuery, button: Button, manager: DialogManager):
    await manager.next()
