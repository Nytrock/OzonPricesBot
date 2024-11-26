from aiogram_dialog import Window, Dialog
from aiogram_dialog.widgets.kbd import Button

from handlers.main_menu import to_main_menu
from states.states import AdminDialogStates
from utils.dialog import Translate

statistic = Window(
    Translate('statistics_users'),
    Button(Translate('back'), id='statistic_back', on_click=to_main_menu),
    state=AdminDialogStates.statistic
)


add_admin = Window(
    Translate('add_admin'),
    Button(Translate('back'), id='add_admin_back', on_click=to_main_menu),
    state=AdminDialogStates.add_admin
)

dialog = Dialog(
    statistic,
    add_admin
)
