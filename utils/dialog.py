from typing import Callable, Any

from aiogram.types import CallbackQuery
from aiogram_dialog import DialogProtocol, DialogManager, SubManager
from aiogram_dialog.api.internal import RawKeyboard
from aiogram_dialog.widgets.common import WhenCondition
from aiogram_dialog.widgets.kbd import Button, ListGroup
from aiogram_dialog.widgets.text import Format, Multi, Const, Text
from aiogram_dialog.widgets.text.format import _FormatDataStub


# Виджет для перевода текста
class Translate(Format):
    def __init__(self, text: str, when: WhenCondition = None):
        super().__init__(when=when, text='{middleware_data[i18n][' + text + ']}')

    async def _render_text(self, data: dict, manager: DialogManager) -> str:
        if manager.is_preview():
            return self.text.format_map(_FormatDataStub(data=data)).format_map(_FormatDataStub(data=data))
        return self.text.format_map(data).format_map(data)


# Создание селекта на основе enum
def create_enum_select(enum_type, middleware_param: str, on_click: Callable) -> list[Button]:
    result = []
    for enum in enum_type:
        result.extend([
            Button(
                Multi(
                    Const('✓'),
                    Translate(str(enum)),
                    sep=' '
                ),
                id=str(enum.value),
                on_click=on_click,
                when=(lambda en: lambda data, _0, _1: data['middleware_data'][middleware_param] == en.value)(enum)
            ),
            Button(
                Translate(str(enum)),
                id=str(enum.value),
                on_click=on_click,
                when=(lambda en: lambda data, _0, _1: data['middleware_data'][middleware_param] != en.value)(enum)
            ),
        ])
    return result


# Кастомный список, сохраняющий id предмета
class CustomListGroup(ListGroup):
    async def _process_item_callback(self, callback: CallbackQuery, data: str,
                                     dialog: DialogProtocol, manager: DialogManager) -> bool:
        item_id, callback_data = data.split(':', maxsplit=1)
        callback = callback.model_copy(update={
            'data': callback_data,
            'item_id': item_id
        })
        sub_manager = SubManager(
            widget=self,
            manager=manager,
            widget_id=self.widget_id,
            item_id=item_id,
        )
        for b in self.buttons:
            if await b.process_callback(callback, dialog, sub_manager):
                return True

    async def _render_item(self, pos: int, item: Any, data: dict, manager: DialogManager) -> RawKeyboard:
        kbd: RawKeyboard = []
        data |= {'item': item, 'pos': pos + 1, 'pos0': pos}
        item_id = str(self.item_id_getter(item))
        sub_manager = SubManager(
            widget=self,
            manager=manager,
            widget_id=self.widget_id,
            item_id=item_id,
        )
        for b in self.buttons:
            b_kbd = await b.render_keyboard(data, sub_manager)
            for row in b_kbd:
                for btn in row:
                    if btn.callback_data:
                        btn.callback_data = self._item_callback_data(
                            f"{item_id}:{btn.callback_data}",
                        )
            kbd.extend(b_kbd)
        return kbd
