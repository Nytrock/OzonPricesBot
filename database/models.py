import datetime
from typing import Annotated

from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import mapped_column, Mapped, relationship

from .database import Base

pk = Annotated[int, mapped_column(primary_key=True)]


class User(Base):
    __tablename__ = 'user'

    id: Mapped[pk]
    is_admin: Mapped[bool] = mapped_column(default=False)
    have_card: Mapped[bool]
    show_variations: Mapped[bool]
    show_product_image: Mapped[bool]
    send_notifications: Mapped[bool]

    favorite_products = relationship('Product', secondary='favorite', back_populates='user')


class Product(Base):
    __tablename__ = 'product'

    id: Mapped[pk]
    name: Mapped[str] = mapped_column(String(200))
    rating: Mapped[float]

    users_favorite = relationship('User', secondary='favorite', back_populates='user')


class Price(Base):
    __tablename__ = 'price'

    id: Mapped[pk]
    product: Mapped[int] = mapped_column(ForeignKey('product.id', ondelete='CASCADE'))
    date: Mapped[datetime.date] = mapped_column(default=datetime.date.today())
    card_price: Mapped[int]
    no_card_price: Mapped[int]


class Favorite(Base):
    __tablename__ = 'favorite'

    id: Mapped[pk]
    user: Mapped[int] = mapped_column(ForeignKey('user.id', ondelete='CASCADE'))
    product: Mapped[int] = mapped_column(ForeignKey('product.id', ondelete='CASCADE'))
