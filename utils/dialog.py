from enum import EnumType
from typing import Callable

from aiogram_dialog.widgets.common import WhenCondition
from aiogram_dialog.widgets.kbd import Button
from aiogram_dialog.widgets.text import Format, Multi, Const


class Translate(Format):
    def __init__(self, text: str, when: WhenCondition = None):
        super().__init__(when=when, text='{middleware_data[i18n][' + text + ']}')


def create_enum_select(enum_type: EnumType, middleware_param: str, on_click: Callable) -> list[Button]:
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
