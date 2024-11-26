from aiogram_dialog import Window, Dialog
from aiogram_dialog.widgets.kbd import Button

from handlers.main_menu import to_main_menu
from states.states import ProductsDialogStates
from utils.dialog import Translate

product_search = Window(
    Translate('product_search'),
    Button(Translate('cancel'), id='products_cancel', on_click=to_main_menu),
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
