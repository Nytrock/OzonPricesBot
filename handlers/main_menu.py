from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Button

from states.states import MainMenuDialogStates, SettingsDialogStates, FavoritesDialogStates


async def to_about(_0: CallbackQuery, _1: Button, manager: DialogManager):
    await manager.switch_to(MainMenuDialogStates.about)


async def to_main_menu(_0: CallbackQuery, _1: Button, manager: DialogManager):
    await manager.start(MainMenuDialogStates.main_menu)
