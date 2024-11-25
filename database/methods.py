from sqlalchemy import select

from .database import create_all, session_factory
from .models import User


async def create_tables():
    await create_all()


async def get_user(user_id: int):
    async with session_factory() as session:
        result = await session.get(User, user_id)
        print(result, type(result))
        return result
