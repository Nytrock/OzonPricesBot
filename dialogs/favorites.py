from aiogram_dialog import Window, Dialog
from aiogram_dialog.widgets.kbd import Back, Cancel, Button, Row, SwitchTo
from aiogram_dialog.widgets.text import Format, Const

from handlers.favorites import get_favorites, previous_favorites, next_favorites, open_favorite_product, \
    remove_favorite_product
from states.states import FavoritesDialogStates
from utils.dialog import Translate, CustomListGroup

# Окно избранного
favorites_show = Window(
    Translate('favorites_show'),
    CustomListGroup(
        Button(
            Format('{item[title]}'),
            id='favorite_product',
            on_click=open_favorite_product
        ),
        id='favorite_products_list',
        item_id_getter=lambda item: item['id'],
        items='favorites',
    ),
    Row(
        Button(
            Const('<'),
            id='favorites_back',
            when=lambda data, _0, _1: data['dialog_data']['page_num'] > 1,
            on_click=previous_favorites
        ),
        Button(
            Format('{dialog_data[page_num]}/{dialog_data[max_pages]}'),
            id='favorites_page',
            when=lambda data, _0, _1: data['dialog_data']['max_pages'] > 1
        ),
        Button(
            Const('>'),
            id='favorites_next',
            when=lambda data, _0, _1: data['dialog_data']['page_num'] < data['dialog_data']['max_pages'],
            on_click=next_favorites
        ),
        when=lambda data, _0, _1: data['dialog_data']['max_pages'] > 0
    ),
    Button(
        Translate('favorites_empty'),
        id='favorites_empty',
        when=lambda data, _0, _1: data['dialog_data']['max_pages'] == 0
    ),
    Row(
        Cancel(
            Translate('back'),
            id='favorites_cancel'
        ),
        SwitchTo(
            Translate('favorites_edit_button'),
            id='favorites_edit',
            state=FavoritesDialogStates.favorites_edit,
            when=lambda data, _0, _1: data['dialog_data']['max_pages'] > 0
        ),
    ),
    state=FavoritesDialogStates.favorites_show,
    getter=get_favorites
)


# Окно редактирования избранного
favorites_edit = Window(
    Translate('favorites_edit'),
    CustomListGroup(
        Button(
            Format('❌ {item[title]}'),
            id='favorite_product',
            on_click=remove_favorite_product
        ),
        id='favorite_products_list',
        item_id_getter=lambda item: item['id'],
        items='favorites',
    ),
    Row(
        Button(
            Const('<'),
            id='favorites_back',
            when=lambda data, _0, _1: data['dialog_data']['page_num'] > 1,
            on_click=previous_favorites
        ),
        Button(
            Format('{dialog_data[page_num]}/{dialog_data[max_pages]}'),
            id='favorites_page',
        ),
        Button(
            Const('>'),
            id='favorites_next',
            when=lambda data, _0, _1: data['dialog_data']['page_num'] < data['dialog_data']['max_pages'],
            on_click=next_favorites
        ),
        when=lambda data, _0, _1: data['dialog_data']['max_pages'] > 0,
    ),
    Button(
        Translate('favorites_empty'),
        id='favorites_empty',
        when=lambda data, _0, _1: data['dialog_data']['max_pages'] == 0,
    ),
    Back(Translate('cancel'), id='favorites_cancel'),
    state=FavoritesDialogStates.favorites_edit,
    getter=get_favorites
)


dialog = Dialog(
    favorites_show,
    favorites_edit
)
