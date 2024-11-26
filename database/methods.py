from typing import Any

from sqlalchemy import insert, select

from enums.user_data import UserShowVariations, UserSendNotifications
from .database import create_all, session_factory
from .models import User, Product, Brand


async def create_tables() -> None:
    await create_all()


async def get_user(user_id: int) -> User:
    async with session_factory() as session:
        result = await session.get(User, user_id)
        return result


async def get_all_users() -> list[User]:
    async with session_factory() as session:
        query = select(User)
        result = await session.execute(query)
        return result.all()

async def create_user(user_data: dict[str, Any]) -> None:
    async with session_factory() as session:
        query = insert(User).values([user_data])
        await session.execute(query)
        await session.commit()


async def make_user_admin(user_id: int) -> None:
    async with session_factory() as session:
        user = await session.get(User, user_id)
        if user:
            user.is_admin = True
            await session.commit()
        else:
            await create_admin(user_id)


async def create_admin(user_id: int) -> None:
    user_data = {
        'id': user_id,
        'have_card': False,
        'show_variations': UserShowVariations.only_cheaper.value,
        'show_product_image': True,
        'send_notifications': UserSendNotifications.only_lowering.value,
        'is_admin': True
    }
    await create_user(user_data)


async def get_all_products() -> list[Product]:
    async with session_factory() as session:
        query = select(Product)
        result = await session.execute(query)
        return result.all()


async def get_all_brands() -> list[Brand]:
    async with session_factory() as session:
        query = select(Brand)
        result = await session.execute(query)
        return result.all()
