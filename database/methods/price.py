from typing import Any

from sqlalchemy import insert, select

from database.database import session_factory
from database.models import Price


async def create_product_price(product_data: dict[str, Any]) -> None:
    async with session_factory() as session:
        query = insert(Price).values(
            product=product_data['id'],
            card_price=product_data['card_price'],
            regular_price=product_data['regular_price'],
            in_stock=product_data['in_stock']
        )
        await session.execute(query)
        await session.commit()


async def get_product_prices(product_id: int) -> list[Price]:
    async with session_factory() as session:
        query = select(Price).filter(Price.product == product_id).order_by(Price.datetime)
        result =  await session.execute(query)
        return result.scalars().all()
