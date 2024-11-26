from aiogram_dialog import Window, Dialog
from aiogram_dialog.widgets.kbd import Button, Cancel
from aiogram_dialog.widgets.text import Multi, Format

from states.states import SettingsDialogStates
from utils.dialog import Translate

all_settings = Window(
    Multi(
        Translate('settings_all'),
        Format('{event.from_user.username}'),
        sep=' '
    ),
    Cancel(Translate('back'), id='settings_back'),
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
