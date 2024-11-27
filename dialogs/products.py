from aiogram.enums import ContentType
from aiogram_dialog import Window, Dialog
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Cancel
from aiogram_dialog.widgets.text import Format

from handlers.products import search_product
from states.states import ProductsDialogStates
from utils.dialog import Translate, DataStaticMedia

product_search = Window(
    Translate('product_search'),
    MessageInput(search_product, content_types=[ContentType.TEXT]),
    Cancel(Translate('cancel'), id='products_cancel'),
    state=ProductsDialogStates.product_search
)


product_search_list = Window(
    state=ProductsDialogStates.product_search_list
)


product_detail = Window(
    DataStaticMedia(
        url='{dialog_data[product][image]}',
        type=ContentType.PHOTO,
        when=lambda data, _0, _1: data['middleware_data']['user_show_image']
    ),
    Format('{dialog_data[product]}'),
    Cancel(Translate('back'), id='products_detail_cancel'),
    state=ProductsDialogStates.product_detail
)


dialog = Dialog(
    product_search,
    product_search_list,
    product_detail
)
