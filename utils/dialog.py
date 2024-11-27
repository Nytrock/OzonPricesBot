from enum import EnumType
from pathlib import Path
from typing import Callable, Union

from aiogram.enums import ContentType
from aiogram_dialog.widgets.common import WhenCondition
from aiogram_dialog.widgets.kbd import Button
from aiogram_dialog.widgets.media import StaticMedia
from aiogram_dialog.widgets.text import Format, Multi, Const, Text


class Translate(Format):
    def __init__(self, text: str, when: WhenCondition = None):
        super().__init__(when=when, text='{middleware_data[i18n][' + text + ']}')


class DataStaticMedia(StaticMedia):
    def __init__(self, *, path: Union[Text, str, Path, None] = None, url: Union[Text, str, None] = None,
                 type: ContentType = ContentType.PHOTO, use_pipe: bool = False, media_params: dict = None,
                 when: WhenCondition = None, data=None):
        super().__init__(path=path, url=url, type=type, use_pipe=use_pipe, media_params=media_params, when=when)
        if self.url is not None:
            self.url = Format(self.url.text)


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
