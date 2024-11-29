from typing import Any

from sqlalchemy import delete, insert, select
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import selectinload

from database.database import session_factory
from database.models import Favorite, User


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


async def is_favorite_exists(user_id: int, product_id: int) -> bool:
    async with session_factory() as session:
        query = select(Favorite).filter(Favorite.user == user_id, Favorite.product == product_id)
        favorite_data = await session.execute(query)

        try:
            favorite_data.scalar_one()
            return True
        except NoResultFound:
            return False


async def get_user_favorites(user_id: int) -> list[dict[str, Any]]:
    async with session_factory() as session:
        query = select(User).filter(User.id == user_id).options(selectinload(User.favorite_products))
        data = await session.execute(query)
        favorites = data.scalar_one().favorite_products

        result = []
        for product in favorites:

            result.append({
                'id': product.id,
                'title': product.title
            })
        return result


async def remove_favorite(user_id: int, product_id: int) -> None:
    async with session_factory() as session:
        query = delete(Favorite).where(Favorite.user == user_id, Favorite.product == product_id)
        await session.execute(query)
        await session.commit()
