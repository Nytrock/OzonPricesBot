from aiogram_dialog import Window, Dialog
from aiogram_dialog.widgets.kbd import Cancel, SwitchTo, Row, Button
from aiogram_dialog.widgets.text import Multi, Format, Const

from enums.user_data import UserShowVariations, UserSendNotifications
from handlers.settings import update_user_have_card, update_user_show_variations, \
    update_user_send_notifications
from states.states import SettingsDialogStates
from utils.dialog import Translate, create_enum_select

all_settings = Window(
    Translate('settings_all'),
    Row(
        SwitchTo(
            Translate('settings_have_card'),
            id='have_card_change',
            state=SettingsDialogStates.have_card
        ),
        SwitchTo(
            Translate('settings_send_notifications'),
            id='send_notifications_change',
            state=SettingsDialogStates.send_notifications
        ),
    ),
    SwitchTo(
        Translate('settings_show_variations'),
        id='show_variants_change',
        state=SettingsDialogStates.show_variants
    ),
    Cancel(Translate('back'), id='settings_back'),
    state=SettingsDialogStates.all_settings
)


have_card = Window(
    Translate('have_card_description'),
    Button(
        Multi(
            Const('[x]'),
            Translate('have_card_checkbox'),
            sep=' '
        ),
        id='off',
        on_click=update_user_have_card,
        when=lambda data, _0, _1: data['middleware_data']['user_have_card']
    ),
    Button(
        Multi(
            Const('[ ]'),
            Translate('have_card_checkbox'),
            sep=' '
        ),
        id='on',
        on_click=update_user_have_card,
        when=lambda data, _0, _1: not data['middleware_data']['user_have_card']
    ),
    SwitchTo(
        Translate('back'),
        id='have_card_back',
        state=SettingsDialogStates.all_settings
    ),
    state=SettingsDialogStates.have_card
)


show_variations = Window(
    Translate('show_variations_description'),
    *create_enum_select(UserShowVariations, 'user_show_variations', update_user_show_variations),
    SwitchTo(
        Translate('back'),
        id='show_variations_back',
        state=SettingsDialogStates.all_settings
    ),
    state=SettingsDialogStates.show_variants
)


send_notifications = Window(
    Translate('send_notifications_description'),
    *create_enum_select(UserSendNotifications, 'user_send_notifications', update_user_send_notifications),
    SwitchTo(
        Translate('back'),
        id='send_notifications_back',
        state=SettingsDialogStates.all_settings
    ),
    state=SettingsDialogStates.send_notifications
)


dialog = Dialog(
    all_settings,
    have_card,
    show_variations,
    send_notifications,
)
