from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import DeclarativeBase

from config_data.config import load_config

db_config = load_config().db
engine = create_async_engine(
    url=f'sqlite+aiosqlite:///{db_config.name}',
    echo=db_config.echo,
)

class Base(DeclarativeBase):
    pass

async def create_all():
    async with engine.begin() as conn:
        from .models import User, Product, Price, Favorite
        await conn.run_sync(Base.metadata.create_all)
