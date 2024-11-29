from aiogram import F
from aiogram.enums import ContentType
from aiogram_dialog import Window, Dialog
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Cancel, Group, Button, Row, SwitchTo, Back
from aiogram_dialog.widgets.text import Format, Multi, Const, Jinja

from handlers.products import search_product, change_variations_mode, change_product, change_product_favorite, \
    previous_search_page, next_search_page, product_detail_start, previous_variations, next_variations
from states.states import ProductsDialogStates
from utils.dialog import Translate, DataStaticMedia, CustomListGroup


product_search = Window(
    Translate('product_get_id'),
    MessageInput(search_product, content_types=[ContentType.TEXT]),
    Cancel(Translate('cancel'), id='products_cancel'),
    state=ProductsDialogStates.product_get_id
)


product_search_list = Window(
    Translate(
        'product_search',
        when=lambda data, _0, _1: data['dialog_data']['have_search_result'],
    ),
    Translate(
        'product_search_error',
        when=lambda data, _0, _1: not data['dialog_data']['have_search_result'],
    ),
    CustomListGroup(
        Button(
            Format('{item[title]}'),
            on_click=change_product,
            id='search_result'
        ),
        id='search_results_list',
        item_id_getter=lambda item: item['id'],
        items=F['dialog_data']['search_products'],
    ),
    Row(
        Button(
            Const('<'),
            id='products_search_back',
            when=lambda data, _0, _1: data['dialog_data']['search_page'] > 1,
            on_click=previous_search_page
        ),
        Button(
            Format('{dialog_data[search_page]}'),
            id='products_search_page',
        ),
        Button(
            Const('>'),
            id='products_search_next',
            on_click=next_search_page
        ),
        when=lambda data, _0, _1: data['dialog_data']['have_search_result'],
    ),
    SwitchTo(
        Translate('back'),
        id='products_search_cancel',
        state=ProductsDialogStates.product_get_id
    ),
    state=ProductsDialogStates.product_search,
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
            id='products_detail_cancel',
            when=lambda data, _0, _1: not data['dialog_data'].get('have_search_result')
        ),
        Back(
            Translate('close'),
            id='products_detail_back',
            when=lambda data, _0, _1: data['dialog_data'].get('have_search_result')
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
            items='variations_limit',
        ),
        Row(
            Button(
                Const('<'),
                id='variations_back',
                when=lambda data, _0, _1: data['dialog_data']['page_num'] > 1,
                on_click=previous_variations
            ),
            Button(
                Format('{dialog_data[page_num]}/{dialog_data[variation_pages]}'),
                id='variations_page',
            ),
            Button(
                Const('>'),
                id='variations_next',
                when=lambda data, _0, _1: data['dialog_data']['page_num'] < data['dialog_data']['variation_pages'],
                on_click=next_variations
            )
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
    state=ProductsDialogStates.product_detail,
    getter=product_detail_start
)


dialog = Dialog(
    product_search,
    product_search_list,
    product_detail,
)
