from aiogram import F
from aiogram.enums import ContentType
from aiogram_dialog import Window, Dialog
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Cancel, Group, Button
from aiogram_dialog.widgets.text import Format, Multi, Const, Jinja

from handlers.products import search_product, change_variations_mode, change_product, change_product_favorite
from states.states import ProductsDialogStates
from utils.dialog import Translate, DataStaticMedia, CustomListGroup

product_search = Window(
    Translate('product_get_id'),
    MessageInput(search_product, content_types=[ContentType.TEXT]),
    Cancel(Translate('cancel'), id='products_cancel'),
    state=ProductsDialogStates.product_get_id
)


product_search_list = Window(
    Translate('product_search'),
    state=ProductsDialogStates.product_search
)


product_detail = Window(
    DataStaticMedia(
        url='{dialog_data[product][image]}',
        type=ContentType.PHOTO,
        when=lambda data, _0, _1: data['middleware_data']['user_show_image']
    ),
    Jinja(
        '<b><a href="https://www.ozon.ru/product/{{ dialog_data.product.id }}">{{ dialog_data.product.title }}</a></b>'
    ),
    Const(' '),
    Translate(
        'product_price_have_card',
        when=lambda data, _0, _1: data['middleware_data']['user_have_card']
    ),
    Translate(
        'product_price_no_card',
        when=lambda data, _0, _1: not data['middleware_data']['user_have_card']
    ),
    Const(' '),
    Translate('product_rating_count'),
    Group(
        Button(
            Translate('product_show_variations'),
            on_click=change_variations_mode,
            id='product_show_variations'
        ),
        Button(
            Translate('product_to_favorites'),
            on_click=change_product_favorite,
            id='product_to_favorites',
            when=lambda data, _0, _1: not data['dialog_data']['into_favorites']
        ),
        Button(
            Translate('product_from_favorites'),
            on_click=change_product_favorite,
            id='product_from_favorites',
            when=lambda data, _0, _1: data['dialog_data']['into_favorites']
        ),
        Cancel(
            Translate('close'),
            id='products_detail_cancel'
        ),
        width=2,
        when=lambda data, _0, _1: not data['dialog_data']['variations_mode']
    ),
    Group(
        CustomListGroup(
            Button(
                Multi(
                    Translate(
                        'product_variant_have_card',
                        when=lambda data, _0, _1: data['middleware_data']['user_have_card']
                    ),
                    Format(
                        'product_variant_no_card',
                        when=lambda data, _0, _1: not data['middleware_data']['user_have_card']
                    ),
                ),
                on_click=change_product,
                id='variations_item'
            ),
            id='variations_list',
            item_id_getter=lambda item: item['id'],
            items=F['dialog_data']['product']['variations'],
        ),
        Button(
            Translate('product_hide_variations'),
            on_click=change_variations_mode,
            id='product_show_variations'
        ),
        when=lambda data, _0, _1: data['dialog_data']['variations_mode'] and data['dialog_data']['have_variations']
    ),
    Group(
        Button(
            Translate('product_no_variations'),
            on_click=change_variations_mode,
            id='product_no_variations'
        ),
        Button(
            Translate('back'),
            on_click=change_variations_mode,
            id='product_show_variations'
        ),
        when=lambda data, _0, _1: data['dialog_data']['variations_mode'] and not data['dialog_data']['have_variations']
    ),
    parse_mode='HTML',
    state=ProductsDialogStates.product_detail
)


dialog = Dialog(
    product_search,
    product_search_list,
    product_detail
)
