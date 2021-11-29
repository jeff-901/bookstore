from backend.store.models import (
    SqlBook,
    SqlCart,
    SqlDiscount,
    SqlOrder,
    SqlOrderItem,
    SqlReview,
    SqlUser,
    Base,
)
from backend.store.sqlalchemy_store import SqlAlchemyStore


class TestSqlAlchemyStore(unittest.TestCase):
    def setUp(self):
        self.db_uri = "mysql+pymysql://bookstore:password@localhost:3306/bookstoretest"
        self.store = SqlAlchemyStore(self.db_uri)

    def tearDown(self):
        Base.metadata.drop_all(self.store.engine)

    def create_user(self):
        name = "user"
        first_name = "jeff"
        last_name = "liu"
