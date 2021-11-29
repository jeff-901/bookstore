from datetime import datetime

import sqlalchemy as sa
from sqlalchemy import (
    BigInteger,
    Boolean,
    Column,
    ForeignKey,
    ForeignKeyConstraint,
    Integer,
    PrimaryKeyConstraint,
    String,
    Text,
)
from sqlalchemy.dialects.mysql import DATETIME
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from entities import User, Book, Cart, Order

Base = declarative_base()


class SqlUser(Base):
    __tablename__ = "user"

    user_id = Column(Integer, nullable=False)
    role = Column(Integer, nullable=False)
    first_name = Column(String(128), nullable=False)
    last_name = Column(String(128), nullable=False)
    email = Column(String(256), nullable=False)
    phone = Column(String(64), nullable=False)
    gender = Column(String(32), nullable=False)
    password = Column(String(256), nullable=False)
    address = Column(String(256), nullable=True)

    orders = relationship("SqlOrder", back_populates="user", cascade="all")
    cart = relationship("SqlCart", back_populates="user", cascade="all")
    reviews = relationship("SqlReview", back_populates="user", cascade="all")

    __table_args__ = (PrimaryKeyConstraint("user_id", name="user_pk"),)

    def __repr__(self):
        return "<SqlUser({}, {}, {}, {}, {}, {}, {}, {}, {})>".format(
            self.user_id,
            self.role,
            self.first_name,
            self.last_name,
            self.email,
            self.phone,
            self.gender,
            self.password,
            self.address,
        )

    def to_entity(self):
        return User(
            user_id=self.user_id,
            role=self.role,
            first_name=self.first_name,
            last_name=self.last_name,
            email=self.email,
            phone=self.phone,
            gender=self.gender,
            address=self.address,
            cart=self.cart,
            orders=self.orders,
        )


class SqlOrder(Base):
    __tablename__ = "order"

    order_id = Column(Integer, nullable=False)
    user_id = Column(
        Integer,
        ForeignKey("user.user_id", onupdate="cascade", ondelete="cascade"),
        nullable=False,
    )
    total_price = Column(Integer, nullable=False)
    time = Column(DATETIME(fsp=3), nullable=False)

    items = relationship("SqlOrderItem", back_populates="order", cascade="all")
    user: SqlUser = relationship("SqlUser", back_populates="orders", cascade="all")

    __table_args__ = (PrimaryKeyConstraint("order_id"),)

    def __repr__(self):
        return "<SqlOrder({}, {}, {}, {})>".format(
            self.order_id,
            self.user_id,
            self.total_price,
            self.time,
        )

    # def to_submarine_entity(self):
    #     return Metric(
    #         key=self.key,
    #         value=self.value if not self.is_nan else float("nan"),
    #         worker_index=self.worker_index,
    #         timestamp=self.timestamp,
    #         step=self.step,
    #     )


class SqlBook(Base):
    __tablename__ = "book"

    book_id = Column(Integer, nullable=False)
    ISBN = Column(String(32), nullable=False)
    name = Column(String(32), nullable=False)
    author = Column(String(32), nullable=False)
    author_original = Column(String(32))
    translator = Column(String(32))
    publishing_house = Column(String(32))
    publishing_date = Column(DATETIME(fsp=3))
    price = Column(Integer, nullable=False)

    discount = relationship("SqlDiscount", back_populates="book", cascade="all")
    reviews = relationship("SqlReview", back_populates="book", cascade="all")

    __table_args__ = (PrimaryKeyConstraint("book_id"),)

    def to_entity(self):
        return Book(
            book_id=self.book_id,
            ISBN=self.ISBN,
            name=self.name,
            author=self.author,
            author_original=self.author_original,
            translator=self.translator,
            publishing_house=self.publishing_house,
            publishing_date=self.publishing_date,
            price=self.price,
            discount_price=self.discount[0].discount_price
            if len(self.discount) > 0
            else None,
            expire_date=self.discount[0].expire_date
            if len(self.discount) > 0
            else None,
        )


class SqlOrderItem(Base):
    __tablename__ = "order_item"

    order_id = Column(
        Integer,
        ForeignKey("order.order_id", onupdate="cascade", ondelete="cascade"),
        nullable=False,
    )
    book_id = Column(
        Integer,
        ForeignKey("book.book_id", onupdate="cascade", ondelete="cascade"),
        nullable=False,
    )
    number = Column(Integer, nullable=False)
    price = Column(Integer, nullable=False)
    order: SqlOrder = relationship("SqlOrder", back_populates="items", cascade="all")

    __table_args__ = (
        PrimaryKeyConstraint("order_id", "book_id", name="order_item_pk"),
    )

    def __repr__(self):
        return "<SqlOrderItem({}, {}, {}, {})>".format(
            self.order_id,
            self.user_id,
            self.number,
            self.price,
        )

    # def to_submarine_entity(self):
    #     return Metric(
    #         key=self.key,
    #         value=self.value if not self.is_nan else float("nan"),
    #         worker_index=self.worker_index,
    #         timestamp=self.timestamp,
    #         step=self.step,
    #     )


class SqlCart(Base):
    __tablename__ = "cart_item"

    user_id = Column(
        Integer,
        ForeignKey("user.user_id", onupdate="cascade", ondelete="cascade"),
        nullable=False,
    )
    book_id = Column(
        Integer,
        ForeignKey("book.book_id", onupdate="cascade", ondelete="cascade"),
        nullable=False,
    )
    number = Column(Integer, nullable=False)

    user: SqlUser = relationship("SqlUser", back_populates="cart", cascade="all")

    __table_args__ = (PrimaryKeyConstraint("user_id", "book_id", name="cart_pk"),)

    def __repr__(self):
        return "<SqlCart({}, {}, {}, {})>".format(
            self.user_id,
            self.book_id,
            self.number,
            self.price,
        )

    def to_entity(self):
        return Cart(self.book_id, self.number)


class SqlDiscount(Base):
    __tablename__ = "discount"

    book_id = Column(
        Integer,
        ForeignKey("book.book_id", onupdate="cascade", ondelete="cascade"),
        nullable=False,
    )

    expire_date = Column(DATETIME(fsp=3), nullable=True)
    discount_price = Column(Integer, nullable=False)
    book: SqlBook = relationship("SqlBook", back_populates="discount", cascade="all")

    __table_args__ = (PrimaryKeyConstraint("book_id"),)

    def __repr__(self):
        return "<SqlDiscount({}, {}, {})>".format(
            self.book_id,
            self.expire_date,
            self.discount_price,
        )


class SqlReview(Base):
    __tablename__ = "review"

    review_id = Column(Integer, nullable=False)

    user_id = Column(
        Integer,
        ForeignKey("user.user_id", onupdate="cascade", ondelete="cascade"),
        nullable=False,
    )
    book_id = Column(
        Integer,
        ForeignKey("book.book_id", onupdate="cascade", ondelete="cascade"),
        nullable=False,
    )
    create_time = Column(DATETIME(fsp=3), nullable=True)
    last_modified = Column(DATETIME(fsp=3), nullable=True)

    user: SqlUser = relationship("SqlUser", back_populates="reviews", cascade="all")
    book: SqlBook = relationship("SqlBook", back_populates="reviews", cascade="all")

    __table_args__ = (PrimaryKeyConstraint("user_id", "book_id", name="review_pk"),)

    def __repr__(self):
        return "<SqlReview({}, {}, {}, {}, {})>".format(
            self.user_id,
            self.book_id,
            self.create_time,
            self.last_modified,
            self.comment,
        )
