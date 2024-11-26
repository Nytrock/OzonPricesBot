from aiogram_dialog import Window, Dialog
from aiogram_dialog.widgets.kbd import Button, Back, Cancel

from states.states import FavoritesDialogStates
from utils.dialog import Translate

favorites_show = Window(
    Translate('favorites_show'),
    Cancel(Translate('back'), id='favorites_back'),
    state=FavoritesDialogStates.favorites_show
)


favorites_edit = Window(
    Translate('favorites_edit'),
    Back(Translate('cancel'), id='favorites_cancel'),
    state=FavoritesDialogStates.favorites_edit
)


dialog = Dialog(
    favorites_show,
    favorites_edit
)
