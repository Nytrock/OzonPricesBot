from aiogram_dialog import Window, Dialog
from aiogram_dialog.widgets.kbd import Button, Cancel

from states.states import ProductsDialogStates
from utils.dialog import Translate

product_search = Window(
    Translate('product_search'),
    Cancel(Translate('cancel'), id='products_cancel'),
    state=ProductsDialogStates.product_search
)


product_search_list = Window(
    state=ProductsDialogStates.product_search_list
)


product_detail = Window(
    state=ProductsDialogStates.product_detail
)


dialog = Dialog(
    product_search,
    product_search_list,
    product_detail
)
