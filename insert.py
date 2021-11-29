from store.sqlalchemy_store import SqlAlchemyStore

store = SqlAlchemyStore("mysql+pymysql://bookstore:password@localhost:3306/bookstore")
store.create_user(
    {
        "role": 0,
        "first_name": "jhan-shuo",
        "last_name": "liu",
        "email": "213@123.com",
        "phone": "886",
        "gender": "male",
        "password": "rew",
    }
)
