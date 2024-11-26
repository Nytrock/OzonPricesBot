from aiogram_dialog import DialogManager, Window, Dialog
from enums.user_data import UserRole

from handlers.admin import to_stats_admin, to_add_admin
from handlers.favorites import to_favorites
from handlers.main_menu import to_about
from handlers.products import to_product_search
from handlers.settings import to_settings

from states.states import MainMenuDialogStates
from aiogram_dialog.widgets.common import Whenable
from aiogram_dialog.widgets.kbd import Row, Button, Back
from aiogram_dialog.widgets.text import Format, Const, Multi

from utils.dialog import Translate


def is_admin(data: dict, widget: Whenable, manager: DialogManager) -> bool:
    return data['middleware_data']['user_role'] == UserRole.admin


main_menu = Window(
    Multi(
        Translate('main_menu_hello'),
        Format('{event.from_user.username}'),
        Const('!'),
        sep=''
    ),
    Multi(
        Const('\n'),
        Translate('main_menu_hello_2'),
        sep=''
    ),
    Button(Translate('main_menu_products'), id='products', on_click=to_product_search),
    Row(
        Button(
            Translate('main_menu_settings'),
            id='settings',
            on_click=to_settings
        ),
        Button(
            Translate('main_menu_favorites'),
            id='favorites',
            on_click=to_favorites
        ),
    ),
    Row(
        Button(
            Translate('main_menu_statistics'),
            id='admin_users',
            on_click=to_stats_admin,
            when=is_admin
        ),
        Button(
            Translate('main_menu_add_admin'),
            id='admin_products',
            on_click=to_add_admin,
            when=is_admin
        ),
    ),
    Button(
        Translate('main_menu_about'),
        id='about',
        on_click=to_about
    ),
    state=MainMenuDialogStates.main_menu,
)


about = Window(
    Translate('about'),
    Back(Translate('back')),
    state=MainMenuDialogStates.about
)


dialog = Dialog(
    main_menu,
    about
)
