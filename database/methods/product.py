from sqlalchemy import select, insert
from sqlalchemy.dialects.postgresql import Any
from sqlalchemy.exc import NoResultFound

from exernal_services.ozon_scrapper import get_product_info_by_id
from ..database import session_factory
from ..models import Product, Seller, ProductGroup


async def get_all_products() -> list[Product]:
    async with session_factory() as session:
        query = select(Product)
        result = await session.execute(query)
        return result.all()


async def get_all_brands() -> list[Seller]:
    async with session_factory() as session:
        query = select(Seller)
        result = await session.execute(query)
        return result.all()


async def get_product_info(product_id: int) -> dict[str, Any]:
    async with session_factory() as session:
        query = select(Product).filter(Product.id == product_id).join(Seller, Seller.id == Product.seller)
        result = await session.execute(query)

        try:
            product = result.scalar_one()
            product_data = {
                'id': product.id,
                'title': product.title,
                'rating': product.rating,
                'rating_count': product.rating_count,
                'description': product.description,
                'image': product.image,
            }

            seller = await session.get(Seller, product.seller)
            product_data['seller'] = seller.name
            return product_data
        except NoResultFound:
            product_data = await get_product_info_by_id(product_id)
            if product_data == {}:
                return {}
            else:
                await create_product(product_data.copy())
                for key in ['variations', 'card_price', 'regular_price']:
                    product_data.pop(key)
                return product_data


async def create_product(product_data: dict[str, Any]) -> None:
    async with session_factory() as session:
        product_data.pop('card_price')
        product_data.pop('regular_price')

        variations = list(product_data.pop('variations'))
        seller_name = product_data.pop('seller')

        query = select(Seller).filter(Seller.name == seller_name)
        seller_data = await session.execute(query)

        try:
            seller = seller_data.scalar_one()
        except NoResultFound:
            await create_brand(seller_name)
            seller_data = await session.execute(query)
            seller = seller_data.scalar_one()
        product_data['seller'] = seller.id

        query = select(ProductGroup).order_by(ProductGroup.id.desc()).limit(1)
        group_id = len((await session.execute(query)).all()) + 1
        await create_product_group(group_id)
        product_data['product_group'] = group_id

        values = [product_data]
        for variation in variations:
            variation_data = await get_product_info_by_id(variation)
            for key in ['variations', 'seller', 'card_price', 'regular_price']:
                variation_data.pop(key)
            variation_data['seller'] = seller.id
            variation_data['product_group'] = group_id
            values.append(variation_data)

        query = insert(Product).values(values)
        await session.execute(query)
        await session.commit()


async def create_brand(brand_name: str) -> None:
    async with session_factory() as session:
        query = insert(Seller).values(name=brand_name)
        await session.execute(query)
        await session.commit()


async def create_product_group(group_id: int) -> None:
    async with session_factory() as session:
        query = insert(ProductGroup).values(id=group_id)
        await session.execute(query)
        await session.commit()
