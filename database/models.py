from typing import Annotated

from datetime import datetime

from sqlalchemy import String, ForeignKey, DateTime, Column
from sqlalchemy.orm import mapped_column, Mapped, relationship

from .database import Base

pk = Annotated[int, mapped_column(primary_key=True)]


class User(Base):
    __tablename__ = 'user'

    id: Mapped[pk]
    is_admin: Mapped[bool] = mapped_column(default=False)
    have_card: Mapped[bool]
    show_variations: Mapped[int]
    send_notifications: Mapped[int]

    favorite_products: Mapped[list['Product']] = relationship(
        secondary='favorite',
        back_populates='users_favorite'
    )


class Product(Base):
    __tablename__ = 'product'

    id: Mapped[pk]
    title: Mapped[str] = mapped_column(String(200))
    rating: Mapped[float]
    rating_count: Mapped[int]
    seller_id: Mapped[int] = mapped_column(ForeignKey('seller.id', ondelete='CASCADE'))
    description: Mapped[str]
    image: Mapped[str]
    product_group: Mapped[int] = mapped_column(ForeignKey('product_group.id', ondelete='CASCADE'))

    users_favorite: Mapped[list['User']] = relationship(
        secondary='favorite',
        back_populates='favorite_products'
    )

    seller: Mapped['Seller'] = relationship(lazy='joined')


class Price(Base):
    __tablename__ = 'price'

    id: Mapped[pk]
    product: Mapped[int] = mapped_column(ForeignKey('product.id', ondelete='CASCADE'))
    datetime = Column(DateTime(timezone=True), default=datetime.now)
    card_price: Mapped[int]
    regular_price: Mapped[int]
    in_stock: Mapped[bool]


class Favorite(Base):
    __tablename__ = 'favorite'

    id: Mapped[pk]
    user: Mapped[int] = mapped_column(ForeignKey('user.id', ondelete='CASCADE'))
    product: Mapped[int] = mapped_column(ForeignKey('product.id', ondelete='CASCADE'))


class ProductGroup(Base):
    __tablename__ = 'product_group'

    id: Mapped[pk]

class Seller(Base):
    __tablename__ = 'seller'

    id: Mapped[pk]
    name: Mapped[str]
