from aiogram.filters import BaseFilter
from aiogram.types import Message

from enums.user_data import UserRole


class RegistrationFilter(BaseFilter):
    def __init__(self, possible_replies: list[str] = None) -> None:
        self.possible_replies = possible_replies

    async def __call__(self,  message: Message, i18n: dict[str, str]) -> bool:
        for possible_reply in self.possible_replies:
            if message.text.lower() == i18n.get(possible_reply).lower():
                return True
        return False


class IsUserRegistered(BaseFilter):
    async def __call__(self, message: Message, user_role: UserRole) -> bool:
        return user_role != UserRole.none
