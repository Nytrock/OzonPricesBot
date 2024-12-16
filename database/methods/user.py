from typing import Any

from sqlalchemy import insert, select

from enums.user_data import UserShowVariations, UserSendNotifications
from ..database import session_factory
from ..models import User


# Получение пользователя
async def get_user(user_id: int) -> User:
    async with session_factory() as session:
        result = await session.get(User, user_id)
        return result


# Получение всех пользователей
async def get_all_users() -> list[User]:
    async with session_factory() as session:
        query = select(User)
        result = await session.execute(query)
        return result.all()


# Создание пользователя
async def create_user(user_data: dict[str, Any]) -> None:
    async with session_factory() as session:
        query = insert(User).values([user_data])
        await session.execute(query)
        await session.commit()


# Сделать пользователя админом
async def make_user_admin(user_id: int) -> None:
    async with session_factory() as session:
        user = await session.get(User, user_id)
        if user:
            user.is_admin = True
            await session.commit()
        else:
            await create_admin(user_id)


# Сохдание пользователя-админа
async def create_admin(user_id: int) -> None:
    user_data = {
        'id': user_id,
        'have_card': False,
        'show_variations': UserShowVariations.only_cheaper.value,
        'send_notifications': UserSendNotifications.only_lowering.value,
        'is_admin': True
    }
    await create_user(user_data)


# Обновление настройки Ozon карты
async def update_have_card(user_id: int, have_card: bool) -> None:
    async with session_factory() as session:
        user = await session.get(User, user_id)
        user.have_card = have_card
        await session.commit()


# Обновление настройки отображения вариаций
async def update_show_variations(user_id: int, show_variations: int) -> None:
    async with session_factory() as session:
        user = await session.get(User, user_id)
        user.show_variations = show_variations
        await session.commit()


# Обновление настройки отправки уведомления
async def update_send_notifications(user_id: int, send_notifications: int) -> None:
    async with session_factory() as session:
        user = await session.get(User, user_id)
        user.send_notifications = send_notifications
        await session.commit()
