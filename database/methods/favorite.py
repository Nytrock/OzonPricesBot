from sqlalchemy import delete, insert, select
from sqlalchemy.exc import NoResultFound

from database.database import session_factory
from database.models import Favorite


async def change_favorite(user_id: int, product_id: int) -> bool:
    async with session_factory() as session:
        favorite_exists = await is_favorite_exists(user_id, product_id)

        if favorite_exists:
            query = delete(Favorite).where(Favorite.user == user_id, Favorite.product == product_id)
        else:
            query = insert(Favorite).values(user=user_id, product=product_id)
        await session.execute(query)
        await session.commit()

        return not favorite_exists


async def is_favorite_exists(user_id: int, product_id: int):
    async with session_factory() as session:
        query = select(Favorite).filter(Favorite.user == user_id, Favorite.product == product_id)
        favorite_data = await session.execute(query)

        try:
            favorite_data.scalar_one()
            return True
        except NoResultFound:
            return False
