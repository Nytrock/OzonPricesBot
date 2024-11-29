from typing import Any

from sqlalchemy import insert

from database.database import session_factory
from database.models import Price


async def create_product_price(product_data: dict[str, Any]) -> None:
    async with session_factory() as session:
        query = insert(Price).values(
            product=product_data['id'],
            card_price=product_data['card_price'],
            regular_price=product_data['regular_price']
        )
        await session.execute(query)
        await session.commit()