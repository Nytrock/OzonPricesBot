from aiogram.filters import BaseFilter
from aiogram.types import Message

from enums.user_data import UserRole


class IsUserAdmin(BaseFilter):
    async def __call__(self, message: Message, user_role: UserRole) -> bool:
        return user_role == UserRole.admin


class IsUserNone(BaseFilter):
    async def __call__(self, message: Message, user_role: UserRole) -> bool:
        return user_role == UserRole.none


class IsUserRegistered(BaseFilter):
    async def __call__(self, message: Message, user_role: UserRole) -> bool:
        return user_role != UserRole.none
