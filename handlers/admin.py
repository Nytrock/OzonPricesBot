from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Button

from states.states import AdminDialogStates


async def to_stats_admin(_0: CallbackQuery, _1: Button, manager: DialogManager):
    await manager.start(AdminDialogStates.statistic)


async def to_add_admin(_0: CallbackQuery, _1: Button, manager: DialogManager):
    await manager.start(AdminDialogStates.add_admin)
