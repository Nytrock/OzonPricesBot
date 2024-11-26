from aiogram.enums import ContentType
from aiogram_dialog import Window, Dialog
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Cancel
from aiogram_dialog.widgets.text import Format, Multi

from handlers.admin import get_admin_statistic, add_new_admin
from states.states import AdminDialogStates
from utils.dialog import Translate

statistic = Window(
    Multi(
        Translate('statistics_users'),
        Format('{users_count}'),
        sep=' '
    ),
    Multi(
        Translate('statistics_products'),
        Format('{products_count}'),
        sep=' '
    ),
    Multi(
        Translate('statistics_brands'),
        Format('{brands_count}'),
        sep=' '
    ),
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
