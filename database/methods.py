from .database import create_all


async def create_tables():
    await create_all()
