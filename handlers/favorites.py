from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Button

from states.states import FavoritesDialogStates


async def to_favorites(_0: CallbackQuery, _1: Button, manager: DialogManager):
    await manager.start(FavoritesDialogStates.favorites_show)