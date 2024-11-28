from aiogram_dialog import Window, Dialog

from enums.user_data import UserRole
from states.states import MainMenuDialogStates, ProductsDialogStates, SettingsDialogStates, FavoritesDialogStates, \
    AdminDialogStates
from aiogram_dialog.widgets.kbd import Row, Back, Start, Next
from aiogram_dialog.widgets.text import Format, Const, Multi

from utils.dialog import Translate


main_menu = Window(
    Translate('main_menu_hello'),
    Multi(
        Const('\n'),
        Translate('main_menu_hello_2'),
        sep=''
    ),
    Start(Translate('main_menu_products'), id='products', state=ProductsDialogStates.product_get_id),
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
            when=lambda data, _0, _1: data['middleware_data']['user_role'] == UserRole.admin
        ),
        Start(
            Translate('main_menu_add_admin'),
            id='admin_products',
            state=AdminDialogStates.add_admin,
            when=lambda data, _0, _1: data['middleware_data']['user_role'] == UserRole.admin
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
    Back(
        Translate('back'),
        id='about_back'
    ),
    state=MainMenuDialogStates.about
)


dialog = Dialog(
    main_menu,
    about
)
