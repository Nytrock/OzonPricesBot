from aiogram.enums import ContentType
from aiogram_dialog import Window, Dialog
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Cancel

from handlers.admin import get_admin_statistic, add_new_admin
from states.states import AdminDialogStates
from utils.dialog import Translate

statistic = Window(
    Translate('statistics_users'),
    Translate('statistics_products'),
    Translate('statistics_brands'),
    Cancel(Translate('back'), id='statistic_back'),
    state=AdminDialogStates.statistic,
    getter=get_admin_statistic
)


add_admin = Window(
    Translate('add_admin'),
    MessageInput(add_new_admin, content_types=[ContentType.TEXT]),
    Cancel(Translate('cancel'), id='add_admin_back'),
    state=AdminDialogStates.add_admin
)

dialog = Dialog(
    statistic,
    add_admin
)
