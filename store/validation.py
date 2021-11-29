from .exceptions import InvalidParameterException


def validate_order_item(item):

    if len(item) != 2:
        raise InvalidParameterException("order item must be len 2.")
    if not isinstance(item[1], int):
        raise InvalidParameterException("order_item[1] must be int.")


def validate_comment(comment):
    if comment is None and not isinstance(comment, str):
        raise InvalidParameterException("parameter comment must be str.")
    if len(comment) > 2048:
        raise InvalidParameterException("parameter comment len must be <= 2048.")
    if len(comment) == 0:
        raise InvalidParameterException(
            "parameter comment must contain at least a character."
        )


def validate_user(body):
    if not isinstance(body, dict):
        raise InvalidParameterException("User must be dictionary format.")
    if body.get("role") is None:
        raise InvalidParameterException("User must contian role field.")
    if not isinstance(body.get("role"), int):
        raise InvalidParameterException("User's role must be an integer.")
    if body.get("first_name") is None:
        raise InvalidParameterException("User must contian first_name field.")
    if body.get("last_name") is None:
        raise InvalidParameterException("User must contian last_name field.")
    if body.get("email") is None:
        raise InvalidParameterException("User must contian email field.")
    if body.get("phone") is None:
        raise InvalidParameterException("User must contian phone field.")
    if body.get("gender") is None:
        raise InvalidParameterException("User must contian gender field.")
    if body.get("password") is None:
        raise InvalidParameterException("User must contian password field.")


def validate_book(body):
    if not isinstance(body, dict):
        raise InvalidParameterException("Book must be dictionary format.")
    if body.get("book_id") is None:
        raise InvalidParameterException("Book must contian book_id field.")
    if not isinstance(body.get("book_id"), int):
        raise InvalidParameterException("Book's book_id must be an integer.")
    if body.get("ISBN") is None:
        raise InvalidParameterException("Book must contian ISBN field.")
    if body.get("name") is None:
        raise InvalidParameterException("Book must contian name field.")
    if body.get("author") is None:
        raise InvalidParameterException("Book must contian author field.")
    if body.get("price") is None:
        raise InvalidParameterException("Book must contian price field.")
    if not isinstance(body.get("price"), int):
        raise InvalidParameterException("Book's price must be an integer.")
    if body.get("discount_price") is not None and not isinstance(
        body.get("discount_price"), int
    ):
        raise InvalidParameterException("Book's discount_price must be an integer.")


def validate_cart(body):
    if not isinstance(body, dict):
        raise InvalidParameterException("Cart must be dictionary format.")
    if body.get("user_id") is None:
        raise InvalidParameterException("Cart must contian user_id field.")
    if body.get("book_id") is None:
        raise InvalidParameterException("Cart must contian book_id field.")
    if body.get("number") is None:
        raise InvalidParameterException("Cart must contian number field.")
    if not isinstance(body.get("user_id"), int):
        raise InvalidParameterException("Cart's user_id must be an integer.")
    if not isinstance(body.get("book_id"), int):
        raise InvalidParameterException("Cart's book_id must be an integer.")
    if not isinstance(body.get("number"), int):
        raise InvalidParameterException("Cart's number must be an integer.")


def validate_order(body):
    if not isinstance(body, dict):
        raise InvalidParameterException("Order must be dictionary format.")
    if body.get("user_id") is None:
        raise InvalidParameterException("Order must contian user_id field.")
    if not isinstance(body.get("user_id"), int):
        raise InvalidParameterException("Oeder's user_id must be an integer.")
    if body.get("items") is None:
        raise InvalidParameterException("Order must contian items field.")
    if not isinstance(body.get("items"), list):
        raise InvalidParameterException("Order'items must be list.")
    for item in body.get("items"):
        validate_order_item(body)


def validate_order_item(body):
    if not isinstance(body, dict):
        raise InvalidParameterException("OrderItem must be dictionary format.")
    if body.get("book_id") is None:
        raise InvalidParameterException("OrderItem must contian book_id field.")
    if body.get("number") is None:
        raise InvalidParameterException("OrderItem must contian number field.")
    if body.get("price") is None:
        raise InvalidParameterException("OrderItem must contian price field.")
    if not isinstance(body.get("book_id"), int):
        raise InvalidParameterException("OrderItem's book_id must be an integer.")
    if not isinstance(body.get("number"), int):
        raise InvalidParameterException("OrderItem's number must be an integer.")
    if not isinstance(body.get("price"), int):
        raise InvalidParameterException("OrderItem's price must be an integer.")
