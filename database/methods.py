from typing import Any

from sqlalchemy import insert

from .database import create_all, session_factory
from .models import User


async def create_tables() -> None:
    await create_all()


async def get_user(user_id: int) -> User:
    async with session_factory() as session:
        result = await session.get(User, user_id)
        return result

async def create_user(user_data: dict[str, Any]) -> None:
    async with session_factory() as session:
        query = insert(User).values([user_data])
        await session.execute(query)
        await session.commit()
