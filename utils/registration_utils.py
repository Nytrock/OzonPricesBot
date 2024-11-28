from aiogram.types import Message

from enums.user_data import UserShowVariations, UserSendNotifications


def is_message_yes(message: Message, i18n: dict[str, str]) -> bool:
    return message.text.lower() == i18n.get('yes').lower()

def message_to_variations_enum(message: Message, i18n: dict[str, str]) -> int:
    text = message.text.lower()
    if text == i18n.get('registration_variation_all').lower():
        return UserShowVariations.all.value
    else:
        return UserShowVariations.only_cheaper.value


def message_to_notifications_enum(message: Message, i18n: dict[str, str]) -> int:
    text = message.text.lower()
    if text == i18n.get('yes').lower():
        return UserSendNotifications.yes.value
    elif text == i18n.get('no').lower():
        return UserSendNotifications.no.value
    else:
        return UserSendNotifications.only_lowering.value
