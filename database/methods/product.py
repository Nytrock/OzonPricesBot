from typing import Any

from sqlalchemy import select, insert
from sqlalchemy.exc import NoResultFound

from exernal_services.ozon_scrapper import get_product_data_from_ozon
from .price import create_product_price
from ..database import session_factory
from ..models import Product, Seller, ProductGroup, Price


async def get_all_products() -> list[Product]:
    async with session_factory() as session:
        query = select(Product)
        result = await session.execute(query)
        return result.all()


async def get_all_sellers() -> list[Seller]:
    async with session_factory() as session:
        query = select(Seller)
        result = await session.execute(query)
        return result.all()


async def get_product_info(product_id: int) -> dict[str, Any]:
    async with session_factory() as session:
        product = await session.get(Product, product_id)
        if product is not None:
            return await get_data_from_product(product)

        product_data = await get_product_data_from_ozon(product_id)
        if product_data == {}:
            return {}
        else:
            await create_product(product_data)
            return product_data


async def get_data_from_product(product: Product) -> dict[str, Any]:
    product_data = {
        'id': product.id,
        'title': product.title,
        'rating': product.rating,
        'rating_count': product.rating_count,
        'description': product.description,
        'image': product.image,
        'seller': product.seller.name,
        'variations': [],
    }

    async with session_factory() as session:
        query = select(Price).filter(Price.product == product.id).order_by(Price.date.desc()).limit(1)
        price_obj = await session.execute(query)
        price = price_obj.scalar_one()
        product_data['card_price'] = price.card_price
        product_data['regular_price'] = price.regular_price
        product_data['in_stock'] = price.in_stock

        query = select(Product).filter(Product.product_group == product.product_group, Product.id != product.id)
        variations_obj = await session.execute(query)
        variations = variations_obj.scalars()

        for variation in variations:
            query = select(Price).filter(Price.product == variation.id).order_by(Price.date.desc()).limit(1)
            variation_price = (await session.execute(query)).scalar_one()
            data = {
                'id': variation.id,
                'title': variation.title,
                'rating': variation.rating,
                'regular_price': variation_price.regular_price,
                'card_price': variation_price.card_price
            }
            product_data['variations'].append(data)

    return product_data


async def create_product(product_data: dict[str, Any]) -> None:
    async with session_factory() as session:
        variations = list(product_data.pop('variations'))
        product_data_to_create = product_data.copy()
        for key in ['card_price', 'regular_price']:
            product_data_to_create.pop(key)

        seller_name = product_data_to_create.pop('seller')
        query = select(Seller).filter(Seller.name == seller_name)
        seller_data = await session.execute(query)

        try:
            seller = seller_data.scalar_one()
        except NoResultFound:
            await create_seller(seller_name)
            seller_data = await session.execute(query)
            seller = seller_data.scalar_one()
        product_data_to_create['seller_id'] = seller.id

        await create_product_price(product_data)

        await create_product_group(product_data['id'])
        product_data_to_create['product_group'] = product_data['id']

        values = [product_data_to_create]
        product_data['variations'] = []
        for variation in variations:
            variation_data = await get_product_data_from_ozon(variation)
            await create_product_price(variation_data)

            for key in ['variations', 'seller']:
                variation_data.pop(key)
            variation_data['seller_id'] = seller.id
            variation_data['product_group'] = product_data['id']

            values.append(variation_data)
            product_data['variations'].append({
                'id': variation_data['id'],
                'title': variation_data['title'],
                'rating': variation_data['rating'],
                'regular_price': variation_data.pop('regular_price'),
                'card_price': variation_data.pop('card_price')
            })

        query = insert(Product).values(values)
        await session.execute(query)
        await session.commit()


async def create_seller(seller_name: str) -> None:
    async with session_factory() as session:
        query = insert(Seller).values(name=seller_name)
        await session.execute(query)
        await session.commit()


async def create_product_group(group_id: int) -> None:
    async with session_factory() as session:
        query = insert(ProductGroup).values(id=group_id)
        await session.execute(query)
        await session.commit()
