from flask import Flask, Blueprint, request, jsonify, render_template
import flask
from flask_cors import CORS
import os
from dotenv import load_dotenv
from store.sqlalchemy_store import SqlAlchemyStore
from store.exceptions import (
    InvalidParameterException,
    ResourceNotFoundException,
    ServerException,
)

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})

load_dotenv()

url = os.getenv("CLEARDB_DATABASE_URL")
url = "mysql+pymysql://bookstore:password@localhost:3306/bookstore"
print(url)
db = SqlAlchemyStore(f"{url}")


api = Blueprint("api", __name__, url_prefix="/api")
app.register_blueprint(api)


@app.errorhandler(ResourceNotFoundException)
def not_found(e):
    return {"message": str(e)}, 404


@app.errorhandler(InvalidParameterException)
def invalid_parameter(e):
    return {"message": str(e)}, 422


@app.errorhandler(ServerException)
def server_error(e):
    return {"message": str(e)}, 500


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@app.route("/api/signin", methods=["POST"])
def signin():
    body = request.get_json(force=True)
    user = db.signin(body.get("email"), body.get("password"))
    if user:
        return build_reponse(user, f"Successfully signin")
    else:
        return build_reponse(None, f"Incorrect password"), 401


@app.route("/api/user/<id>", methods=["GET", "DELETE", "PUT"])
def user(id):
    if request.method == "GET":
        user = db.get_user(id)
        return build_reponse(user, "Success")
    elif request.method == "DELETE":
        db.delete_user(id)
        return build_reponse(None, f"Successfully delete user with user_id={id}")
    else:
        body = request.get_json(force=True)
        db.update_user(
            id,
            role=body.get("role"),
            first_name=body.get("first_name"),
            last_name=body.get("last_name"),
            phone=body.get("phone"),
            gender=body.get("gender"),
            password=body.get("password"),
            address=body.get("address"),
        )
        return build_reponse(None, f"Successfully update user with user_id={id}")


@app.route("/api/user", methods=["GET", "POST"])
def users():
    if request.method == "GET":
        users = db.list_user()
        return build_reponse(users, "Success")
    else:
        body = request.get_json(force=True)
        user = db.create_user(body)
        return build_reponse(user, "Successfully create"), 201


@app.route("/api/search/user", methods=["GET"])
def search_user():
    email = request.args.get("email", default=None, type=str)
    user = db.search_user(email)
    return build_reponse(user, "Success")


@app.route("/api/book/<id>", methods=["GET", "DELETE"])
def book(id):
    if request.method == "GET":
        book = db.get_book(id)
        return build_reponse(book, "Success")
    elif request.nethod == "DELETE":
        db.delete_book(id)
        return build_reponse(None, f"Successfully delete book with book_id={id}")
    # else:
    #     body = request.get_json(force=True)
    #     db.update_book(book_id, body)
    #     return build_reponse(None, f"Successfully update book with book_id={id}")


@app.route("/api/book", methods=["GET", "POST"])
def books():
    if request.method == "GET":
        books = db.list_book()
        return build_reponse(books, "Success")
    else:
        body = request.get_json(force=True)
        db.create_book(body)
        return build_reponse(None, "Successfully create"), 201


@app.route("/api/search/book", methods=["GET"])
def search_books():
    name = request.args.get("name", default=None, type=str)
    print(name)
    books = db.search_book(name=name)
    return build_reponse(books, "Success")


@app.route("/api/cart", methods=["POST", "DELETE", "PUT", "GET"])
def carts():
    if request.method == "POST":
        body = request.get_json(force=True)
        db.create_cart(body)
        return build_reponse(None, "Successfully create"), 201
    elif request.method == "DELETE":
        user_id = request.args.get("user_id", default=None, type=int)
        if user_id is None:
            raise InvalidParameterException("query user_id must exist.")
        book_id = request.args.get("book_id", default=None, type=int)
        db.delete_cart(user_id, book_id)
        return build_reponse(
            None,
            f"Successfully delete carts with user_id={user_id} and book_id={book_id}",
        )
    elif request.method == "PUT":
        body = request.get_json(force=True)
        db.update_cart(body)
        return build_reponse(
            None,
            f"Successfully update cart with user_id={body['user_id']} and book_id={body['book_id']}",
        )
    else:
        user_id = request.args.get("user_id")
        book_id = request.args.get("book_id")
        cart_item = db.get_cart(user_id, book_id)

        return build_reponse(cart_item, "Success")


@app.route("/api/order/<id>", methods=["GET", "DELETE"])
def order(id):
    if request.method == "GET":
        order = db.get_order(id)
        return build_reponse(order, "Success")
    elif request.nethod == "DELETE":
        db.delete_order(id)
        return build_reponse(None, f"Successfully delete order with order_id={id}")


@app.route("/api/order", methods=["POST"])
def orders():
    # if request.method == "GET":
    #     orders = db.list_order()
    #     return build_reponse(orders, "Success")
    # if:
    body = request.get_json(force=True)
    db.create_order(body)
    return build_reponse(None, "Successfully create"), 201


@app.route("/api/search/order", methods=["GET"])
def search_order():
    user_id = request.args.get("user_id", default=None, type=str)
    orders = db.search_order(user_id)
    return build_reponse(orders, "Success")


def build_reponse(data, message):
    if data is None:
        return {"message": message}
    if isinstance(data, list):
        return {"data": [ele.__dict__ for ele in data], "message": message}
    else:
        return {"data": data.__dict__, "message": message}


if __name__ == "__main__":
    app.run(debug=True)
