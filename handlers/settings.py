from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Button

from states.states import SettingsDialogStates


async def to_settings(_0: CallbackQuery, _1: Button, manager: DialogManager):
    await manager.start(SettingsDialogStates.all_settings)