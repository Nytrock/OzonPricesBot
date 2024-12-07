from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

from callback_factory.callback_factory import ProductCallbackFactory


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

def create_notification_kb(product_id: int,  i18n: dict[str, str]):
    kb_builder = InlineKeyboardBuilder()

    button_product = InlineKeyboardButton(
        text=i18n['notification_button'],
        callback_data=ProductCallbackFactory(
            product_id=product_id,
        ).pack()
    )

    kb_builder.row(button_product)
    return kb_builder.as_markup(
        resize_keyboard=True,
    )
