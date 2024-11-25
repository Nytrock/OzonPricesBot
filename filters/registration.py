from aiogram.filters import BaseFilter
from aiogram.types import Message



class RegistrationFilter(BaseFilter):
    def __init__(self, possible_replies: list[str] = None) -> None:
        self.possible_replies = possible_replies

    async def __call__(self,  message: Message, i18n: dict[str, str]) -> bool:
        for possible_reply in self.possible_replies:
            if message.text.lower() == i18n.get(possible_reply).lower():
                return True
        return False
