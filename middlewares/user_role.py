from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, User

from database.methods import get_user
from enums.user_data import UserRole


class UserRoleMiddleware(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: Dict[str, Any]
    ) -> Any:
        user = await get_user(data.get('event_from_user').id)
        if user is None:
            data['user_role'] = UserRole.none
        elif user.is_admin:
            data['user_role'] = UserRole.admin
        else:
            data['user_role'] = UserRole.default

        data['user_is_admin'] = user.is_admin

        return await handler(event, data)
