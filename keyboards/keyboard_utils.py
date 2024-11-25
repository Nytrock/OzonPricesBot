from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, KeyboardButton, ReplyKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder


def create_inline_kb(i18n: dict[str, str], width: int, *args: str, **kwargs: str) -> InlineKeyboardMarkup:
    kb_builder = InlineKeyboardBuilder()
    buttons: list[InlineKeyboardButton] = []

    if args:
        for button in args:
            buttons.append(InlineKeyboardButton(
                text=i18n[button] if i18n.get(button) else button,
                callback_data=button))
    if kwargs:
        for button, text in kwargs.items():
            buttons.append(InlineKeyboardButton(
                text=text,
                callback_data=button))

    kb_builder.row(*buttons, width=width)
    return kb_builder.as_markup()


def create_reply_kb(i18n: dict[str, str], width: int, *args: str, **kwargs: str) -> ReplyKeyboardMarkup:
    kb_builder = ReplyKeyboardBuilder()
    buttons: list[KeyboardButton] = []

    if args:
        for button in args:
            buttons.append(KeyboardButton(
                text=i18n[button] if i18n.get(button) else button,
                callback_data=button))
    if kwargs:
        for button, text in kwargs.items():
            buttons.append(KeyboardButton(
                text=text,
                callback_data=button))

    kb_builder.row(*buttons, width=width)
    return kb_builder.as_markup(
        resize_keyboard=True,
    )

