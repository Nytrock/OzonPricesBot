from aiogram_dialog.widgets.common import WhenCondition
from aiogram_dialog.widgets.text import Format


class Translate(Format):
    def __init__(self, text: str, when: WhenCondition = None):
        super().__init__(when=when, text='{middleware_data[i18n][' + text + ']}')
