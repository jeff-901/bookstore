from datetime import datetime, timedelta
import sqlalchemy
from sqlalchemy.engine.base import Engine
from sqlalchemy.orm.session import Session
from sqlalchemy.orm import subqueryload
from .models import (
    Base,
    SqlBook,
    SqlCart,
    SqlDiscount,
    SqlOrder,
    SqlOrderItem,
    SqlReview,
    SqlUser,
)

from entities import CartWithBook
from store.exceptions import (
    InvalidParameterException,
    ResourceNotFoundException,
    ServerException,
)
from .validation import (
    validate_order,
    validate_comment,
    validate_user,
    validate_book,
    validate_cart,
)

dateFormatter = "%Y/%m/%d"


class SqlAlchemyStore:
    def __init__(self, db_uri):
        self.db_uri = db_uri
        self.engine = sqlalchemy.create_engine(db_uri)
        insp = sqlalchemy.inspect(self.engine)
        expected_tables = {
            SqlBook.__tablename__,
            SqlCart.__tablename__,
            SqlDiscount.__tablename__,
            SqlOrder.__tablename__,
            SqlOrderItem.__tablename__,
            SqlReview.__tablename__,
            SqlUser.__tablename__,
        }
        for table in expected_tables:
            if table not in set(insp.get_table_names()):
                Base.metadata.tables[table].create(bind=self.engine)

    def _save_to_db(self, session, objs):
        if type(objs) is list:
            session.add_all(objs)
        else:
            session.add(objs)

    def create_user(self, body):
        # TODO check email validation
        validate_user(body)
        with Session(self.engine) as session:
            user = (
                session.query(SqlUser).filter(SqlUser.email == body.get("email")).all()
            )
            if len(user) > 0:
                raise InvalidParameterException(
                    f"User with email={body.get('email')} already exists."
                )

            user = SqlUser(
                role=body.get("role"),
                first_name=body.get("first_name"),
                last_name=body.get("last_name"),
                email=body.get("email"),
                phone=body.get("phone"),
                gender=body.get("gender"),
                password=body.get("password"),
                address=body.get("address"),
            )
            try:
                self._save_to_db(session, user)
                session.commit()
                return user.to_entity()
            except Exception as e:
                raise ServerException(str(e))

    def _get_user(self, session, user_id):
        users = (
            session.query(SqlUser)
            .filter(SqlUser.user_id == user_id)
            .options(
                [
                    subqueryload(SqlUser.cart),
                    subqueryload(SqlUser.orders),
                ]
            )
            .all()
        )
        if len(users) == 0:
            raise ResourceNotFoundException(f"User with id={user_id} not found")
        return users[0]

    def get_user(self, user_id):
        with Session(self.engine) as session:
            return self._get_user(session, user_id).to_entity()

    def signin(self, email, password):
        with Session(self.engine) as session:
            users = session.query(SqlUser).filter(SqlUser.email == email).all()
            if len(users) == 0:
                raise ResourceNotFoundException(f"User with email={email} not found")
            user = users[0]
            if user.password == password:
                return user.to_entity()
            else:
                return False

    def list_user(self):
        with Session(self.engine) as session:
            users = (
                session.query(SqlUser)
                .options(
                    [
                        sqlalchemy.orm.subqueryload(SqlUser.cart),
                        sqlalchemy.orm.subqueryload(SqlUser.orders),
                    ]
                )
                .all()
            )
            return [user.to_entity() for user in users]

    def update_user(
        self,
        user_id,
        role=None,
        first_name=None,
        last_name=None,
        phone=None,
        gender=None,
        password=None,
        address=None,
    ):
        # TODO check detailed validation
        with Session(self.engine) as session:
            user = self._get_user(session, user_id)
            if role is not None:
                user.role = role
            if first_name is not None:
                user.first_name = first_name
            if last_name is not None:
                user.last_name = last_name
            if phone is not None:
                user.phone = phone
            if gender is not None:
                user.gender = gender
            if address is not None:
                user.address = address
            try:
                self._save_to_db(session, user)
                session.commit()
                return user
            except Exception as e:
                raise ServerException(str(e))

    def delete_user(self, user_id):
        with Session(self.engine) as session:
            user = self._get_user(session, user_id)
            # print(user)
            try:
                session.delete(user)
                session.commit()
            except Exception as e:
                session.rollback()
                raise ServerException(str(e))

    def search_user(self, email):
        with Session(self.engine) as session:
            users = session.query(SqlUser).filter(SqlUser.email == email).all()
            if len(users) == 0:
                raise ResourceNotFoundException(f"User with email={email} not found")
            return users[0].to_entity()

    def create_book(self, body):
        validate_book(body)
        with Session(self.engine) as session:
            book = (
                session.query(SqlBook)
                .filter(SqlBook.book_id == body.get("book_id"))
                .all()
            )
            if len(book) > 0:
                raise InvalidParameterException(
                    f"Book with id={body.get('book_id')} already eists."
                )
            expire_date = None
            publishing_date = None
            discount = []
            try:
                if isinstance(body.get("discount"), dict):
                    if (
                        body.get("discount").get("expire_date") is not None
                        and body.get("discount").get("expire_date") != ""
                    ):
                        expire_date = datetime.strptime(
                            body["discount"]["expire_date"], dateFormatter
                        ) + timedelta(hours=23, minutes=59, seconds=59)
                    discount = [
                        SqlDiscount(
                            book_id=body.get("book_id"),
                            discount_price=body.get("discount").get("discount_price"),
                            expire_date=expire_date,
                        ),
                    ]
                if (
                    body.get("publishing_date") is not None
                    and body.get("publishing_date") != ""
                ):
                    publishing_date = datetime.strptime(
                        body["publishing_date"], dateFormatter
                    )
            except Exception as e:
                raise InvalidParameterException(str(e))
            book = SqlBook(
                book_id=body.get("book_id"),
                ISBN=body.get("ISBN"),
                name=body.get("name"),
                author=body.get("author"),
                author_original=body.get("author_original"),
                translator=body.get("translator"),
                publishing_house=body.get("publishing_house"),
                publishing_date=publishing_date,
                price=body.get("price"),
                discount=discount,
            )

            try:
                self._save_to_db(session, book)
                session.commit()
            except Exception as e:
                session.rollback()
                raise ServerException(str(e))

    def _get_book(self, session, book_id):
        books = (
            session.query(SqlBook)
            .filter(SqlBook.book_id == book_id)
            .options([sqlalchemy.orm.subqueryload(SqlBook.discount)])
            .all()
        )
        if len(books) == 0:
            raise ResourceNotFoundException(f"Book with id={book_id} not found")
        return books[0]

    def get_book(self, book_id):
        with Session(self.engine) as session:
            return self._get_book(session, book_id).to_entity()

    def list_book(self):
        with Session(self.engine) as session:
            return [
                book.to_entity()
                for book in session.query(SqlBook)
                .options([sqlalchemy.orm.subqueryload(SqlBook.discount)])
                .all()
            ]

    def delete_book(self, book_id):
        with Session(self.engine) as session:
            book = self._get_book(session, book_id)
            try:
                session.delete(book)
                session.commit()
            except Exception as e:
                session.rollback()
                raise ServerException(str(e))

    def search_book(self, name="", date=datetime(2019, 1, 1)):
        with Session(self.engine) as session:
            return [
                book.to_entity()
                for book in session.query(SqlBook)
                .options([sqlalchemy.orm.subqueryload(SqlBook.discount)])
                .filter(SqlBook.name.like(f"%{name}%"))
                .all()
            ]

    def create_cart(self, body):
        validate_cart(body)
        user_id = body["user_id"]
        book_id = body["book_id"]
        number = body["number"]
        with Session(self.engine) as session:
            self._get_user(session, user_id)
            self._get_book(session, book_id)
            cart = SqlCart(user_id=user_id, book_id=book_id, number=number)
            try:
                old_cart = self._get_cart(session, user_id, book_id)
            except:
                old_cart = None
            if old_cart:
                old_cart.number += cart.number
                try:
                    self._save_to_db(session, old_cart)
                    session.commit()
                except Exception as e:
                    session.rollback()
                    raise ServerException(str(e))
            else:
                try:
                    self._save_to_db(session, cart)
                    session.commit()
                except Exception as e:
                    session.rollback()
                    raise ServerException(str(e))

    def _get_cart(self, session, user_id, book_id):
        carts = (
            session.query(SqlCart)
            .filter(SqlCart.user_id == user_id)
            .filter(SqlCart.book_id == book_id)
            .all(),
        )
        if len(carts) == 0:
            raise ResourceNotFoundException(
                f"Cart with user_id={user_id} and book_id={book_id} not found"
            )
        return carts[0]

    def get_cart(self, user_id, book_id):
        with Session(self.engine) as session:
            self._get_user(session, user_id)
            self._get_book(session, book_id)
            carts = (
                session.query(SqlCart, SqlBook)
                .join(SqlBook)
                .filter(SqlBook.book_id == SqlCart.book_id)
                .filter(SqlCart.user_id == user_id)
                .filter(SqlCart.book_id == book_id)
                .all(),
            )
            if len(carts) == 0:
                raise ResourceNotFoundException(
                    f"Cart with user_id={user_id} and book_id={book_id} not found"
                )
        return carts[0]

    def update_cart(self, body):
        validate_cart(body)
        user_id = body["user_id"]
        book_id = body["book_id"]
        number = body["number"]
        with Session(self.engine) as session:
            cart = self._get_cart(session, user_id, book_id)
            cart.number = number
            try:
                self._save_to_db(session, cart)
                session.commit()
            except Exception as e:
                raise ServerException(str(e))

    def delete_cart(self, user_id, book_id):
        with Session(self.engine) as session:
            if book_id is not None:
                carts = [self._get_cart(session, user_id, book_id)]
            else:
                carts = session.query(SqlCart).filter(SqlCart.user_id == user_id).all()
            try:
                for cart in carts:
                    print(cart)
                    session.delete(cart)
                session.commit()
            except Exception as e:
                session.rollback()
                raise ServerException(str(e))

    def create_order(self, body):
        validate_order(body)
        user_id = body.get("user_id")
        with Session(self.engine) as session:
            user = self._get_user(session, user_id)
            sql_order_items = []
            total_price = 0
            for order_item in body.get("items"):
                book = self._get_book(session, order_item.get("book_id"))
                number = order_item.get("number")
                if book.discount:
                    price = book.discount[0].discount_price
                else:
                    price = book.price
                sql_order_items.append(
                    SqlOrderItem(book_id=book.book_id, number=number, price=price)
                )
                total_price += number * price
            order = SqlOrder(
                user_id=user_id,
                time=datetime.now(),
                total_price=total_price,
                items=sql_order_items,
            )
            try:
                self._save_to_db(session, order)
                session.commit()
            except:
                session.rollback()
                raise ServerException(str(e))

    def _get_order(self, session, order_id):
        orders = session.query(SqlOrder).filter(SqlOrder.order_id == order_id).all()
        if len(orders) == 0:
            raise ResourceNotFoundException(f"Order with order_id={order_id} not found")
        return orders[0]

    def get_order(self, order_id):
        return self._get_order(session, order_id).to_entity()

    def delete_order(self, order_id):
        with Session(self.engine) as session:
            order = self._get_order(session, order_id)
            try:
                session.delete(order)
                session.commit()
            except Exception as e:
                session.rollback()
                raise ServerException(str(e))

    def search_order(self, user_id):
        with Session(self.engine) as session:
            self._get_user(session, user_id)
            orders = session.query(SqlOrder).filter(SqlOrder.user_id == user_id).all()
            return [order.to_entity() for order in orders]

    def create_review(self, user_id, book_id, comment):
        validate_comment(comment)
        with Session(self.engine) as session:
            self._get_user(session, user_id)
            self._get_book(session, book_id)
            validate_review
            review = SqlReview(user_id=user_id, book_id=book_id, comment=comment)
            try:
                self._save_to_db(session, review)
                session.commit()
            except Exception as e:
                raise ServerException(e)

    def _get_review(self, session, review_id):
        reviews = (
            session.query(SqlReview).filter(SqlReview.review_id == review_id).all()
        )
        if len(reviews) == 0:
            raise ResourceNotFoundException(
                f"Review with review_id={review_id} not found"
            )
        return reviews[0]

    def delete_review(self, review_id):
        with Session(self.engine) as session:
            review = self._get_review(session, review_id)
            session.delete(review)
            session.commit()
