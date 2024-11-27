from sqlalchemy import select

from ..database import session_factory
from ..models import Product, Brand

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
