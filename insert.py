from store.sqlalchemy_store import SqlAlchemyStore

store = SqlAlchemyStore(
    "mysql+pymysql://bc107f18a3874b:e9b54d1f@us-cdbr-east-04.cleardb.com/heroku_df25299c540ccc8"
)
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
