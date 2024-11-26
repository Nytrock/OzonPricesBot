from aiogram_dialog import Window, Dialog
from aiogram_dialog.widgets.kbd import Button
from aiogram_dialog.widgets.text import Multi, Format

from handlers.main_menu import to_main_menu
from states.states import SettingsDialogStates
from utils.dialog import Translate

all_settings = Window(
    Multi(
        Translate('settings_all'),
        Format('{event.from_user.username}'),
        sep=' '
    ),
    Button(Translate('back'), id='settings_back', on_click=to_main_menu),
    state=SettingsDialogStates.all_settings
)


have_card = Window(
    state=SettingsDialogStates.have_card
)


show_variants = Window(
    state=SettingsDialogStates.show_variants
)


show_image = Window(
    state=SettingsDialogStates.show_image
)


send_notifications = Window(
    state=SettingsDialogStates.send_notifications
)


dialog = Dialog(
    all_settings,
    have_card,
    show_variants,
    show_image,
    send_notifications
)
