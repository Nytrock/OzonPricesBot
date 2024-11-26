from aiogram_dialog import DialogManager, Window, Dialog
from enums.user_data import UserRole

from states.states import MainMenuDialogStates, ProductsDialogStates, SettingsDialogStates, FavoritesDialogStates, \
    AdminDialogStates
from aiogram_dialog.widgets.common import Whenable
from aiogram_dialog.widgets.kbd import Row, Button, Back, Start, Next
from aiogram_dialog.widgets.text import Format, Const, Multi

from utils.dialog import Translate


def is_admin(data: dict, _0: Whenable, _1: DialogManager) -> bool:
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
    Start(Translate('main_menu_products'), id='products', state=ProductsDialogStates.product_search),
    Row(
        Start(
            Translate('main_menu_settings'),
            id='settings',
            state=SettingsDialogStates.all_settings
        ),
        Start(
            Translate('main_menu_favorites'),
            id='favorites',
            state=FavoritesDialogStates.favorites_show
        ),
    ),
    Row(
        Start(
            Translate('main_menu_statistics'),
            id='admin_users',
            state=AdminDialogStates.statistic,
            when=is_admin
        ),
        Start(
            Translate('main_menu_add_admin'),
            id='admin_products',
            state=AdminDialogStates.add_admin,
            when=is_admin
        ),
    ),
    Next(
        Translate('main_menu_about'),
        id='about',
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
